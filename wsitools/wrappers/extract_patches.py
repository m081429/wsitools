# -*- coding: utf-8 -*-

import argparse
import logging
import os
import sys

from wsitools.tissue_detection.tissue_detector import TissueDetector
from wsitools.patch_extraction.patch_extractor import ExtractorParameters, PatchExtractor
from wsitools.patch_extraction.feature_map_creator import FeatureMapCreator
from wsitools.wsi_annotation.region_annotation import AnnotationRegions
from wsitools.patch_extraction.pairwise_patch_extractor import PairwiseExtractorParameters, PairwisePatchExtractor
from wsitools.wsi_registration.auto_wsi_matcher import MatcherParameters, WSI_Matcher

import multiprocessing

def main():
    """Console script for extracting patches from WSI files."""
    parser = argparse.ArgumentParser()

    parser.add_argument("-w", "--wsi_fn",
                        required=True,
                        dest='wsi_fn',
                        help="WSI file name")

    parser.add_argument("-o", "--out-dir",
                        default=os.getcwd(),
                        dest='out_dir',
                        help="Where patches should be saved")

    parser.add_argument("-s", "--patch-size",
                        default=256,
                        dest='patch_size',
                        type=int,
                        help="H & W of patches")

    parser.add_argument("-n", "--number-processors",
                        default=8,
                        dest='num_processors',
                        type=int,
                        help="Number of processors to use during patch extraction")

    parser.add_argument("-c", "--number-patches",
                        default=-1,
                        dest='sample_cnt',
                        type=int,
                        help="Number of processors to use during patch extraction [-1 == all]")

    parser.add_argument("-a", "--patch-filter-tissue-area",
                        default=0.8,
                        dest='patch_filter_by_area',
                        type=float,
                        help="Amount of tissue that should be present in a patch")

    parser.add_argument("-R", "--rescale-rate",
                        default=128,
                        dest='rescale_rate',
                        type=int,
                        help="Fold size to scale the thumbnail to (for faster processing)")

    parser.add_argument("-f", "--patch-format",
                        dest='save_format',
                        choices=['.png', '.jpg', '.tfrecord'],
                        default=".png",
                        help="Output format for patches")

    parser.add_argument("-x", "--annotation-xml",
                        dest='anno_xml',
                        default=None,
                        help="XML definig the annotations")

    parser.add_argument("-y", "--annotation-class_label_id_csv",
                        dest='anno_class_label_id_csv',
                        default=None,
                        help="XML class_label_id_csv")

    parser.add_argument("-l", "--openslide-level",
                        dest='openslide_level',
                        default=0,
                        help="Level used to extract patches")

    parser.add_argument("-T", "--tissue-detection-method",
                        dest="tissue_detector_method",
                        choices=['LAB_Threshold', 'GNB'],
                        default="LAB_Threshold",
                        help="Choose the method for finding tissue")

    parser.add_argument("-t", "--tissue-detection-threshold",
                        dest="tissue_detector_threshold",
                        choices=range(1, 255),
                        default=80,
                        help="Threshold at which there is tissue in patch (used for LAB_Threshold)")

    parser.add_argument("-G", "--GNB-file",
                        dest="training_file",
                        default=None,
                        help="GNB training file (if GNB method is chosen)")

    parser.add_argument("-F", "--feature-map",
                        dest="feature_map",
                        default=None,
                        help="Feature map file (used if output is TFRecords)")

    parser.add_argument("-W", "--wsi_reg_2",
                        dest='wsi_reg_2',
                        help="second WSI registration file name")

    parser.add_argument("-Ox", "--reg_off_set_x",
                        dest='reg_off_set_x', type=float,
                        help="Registration X offset")

    parser.add_argument("-Oy", "--reg_off_set_y",
                        dest='reg_off_set_y', type=float,
                        help="Registration Y offset")

    parser.add_argument("-V", "--verbose",
                        dest="logLevel",
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default="INFO",
                        help="Set the logging level")

    args = parser.parse_args()
    logging.basicConfig(stream=sys.stderr, level=args.logLevel,
                        format='%(name)s (%(levelname)s): %(message)s')

    logger = logging.getLogger(__name__)
    logger.setLevel(args.logLevel)

    ''' If TFRecords, must have a feature map'''
    if args.save_format == '.tfrecord':
        assert args.feature_map is not None, "You must supply a feature map if you want TFRecords exported"
        assert os.path.exists(args.feature_map), "Your feature map file ({}) was not found".format(args.feature_map)

    '''Required arguments for GNB-based tissue detection'''
    if args.tissue_detector_method == 'GNB':
        assert args.training_file is not None, "You must provide a GNB file if using GNB-based tissue detection"
        assert os.path.exists(args.training_file), "Your GNB file ({}) was not found".format(args.training_file)

    ''' If annotation is provided, change the default output for outputting annotation  If Annotation xml file is provided, must have a XML class_label_id_csv file'''
    with_anno = False
    annotations = None
    if args.anno_xml:
        with_anno = True
        assert os.path.exists(args.anno_xml),  "Your XML file ({}) was not found".format(args.anno_xml)
        assert args.anno_class_label_id_csv is not None, "You must supply a input file"
        assert os.path.exists(args.anno_class_label_id_csv), "Your wsi file ({}) was not found".format(args.anno_class_label_id_csv)

        annotations = AnnotationRegions(args.anno_xml, args.anno_class_label_id_csv)

    '''Setting None if feature_map is not provided'''
    if args.feature_map is not None:
        fm = FeatureMapCreator(args.feature_map)
    else:
        fm = None

    '''Checking input param for image registration'''
    if args.wsi_reg_2 :
        assert os.path.exists(args.wsi_reg_2)

    '''Choose a method for detecting tissue in thumbnail image'''
    tissue_detector = TissueDetector(args.tissue_detector_method,               # Can be LAB_Threshold or GNB
                                     threshold=args.tissue_detector_threshold,  # Number from 1-255, anything less than\
                                                                                # this number means there is tissue
                                     training_files=args.training_file          # Training file for GNB-based detection
                                     )
    '''Is offset values are provided then check values are float'''
    if args.reg_off_set_x or args.reg_off_set_y:
        assert str(args.reg_off_set_x).lstrip('-').replace('.','',1).isdigit()
        assert str(args.reg_off_set_y).lstrip('-').replace('.','',1).isdigit()
        offset = (float(args.reg_off_set_x), float(args.reg_off_set_x))
    else:
        '''Is offset values are not provided then offset values are calculated based on image registration'''
        if args.wsi_reg_2:
            matcher_parameters = MatcherParameters()
            matcher = WSI_Matcher(tissue_detector, matcher_parameters)
            offset = matcher.match(args.wsi_fn, args.wsi_reg_2)

    '''Calling appropriate methods if registration offsets are provided, so this block is called in patch_extraction with image regitration and in patch_extraction with image regitration & annotations'''
    if args.wsi_reg_2 :

        parameters = PairwiseExtractorParameters(args.out_dir,  # Where the patches should be extracted to
                                         save_format=args.save_format,  # Can be '.jpg', '.png', or '.tfrecord'
                                         sample_cnt=args.sample_cnt,  # Limit the number of patches to extract
                                         # (-1 == all patches)
                                         patch_size=args.patch_size,  # Size of patches to extract (Height & Width)
                                         rescale_rate=args.rescale_rate,
                                         # Fold size to scale the thumbnail to (for faster \
                                         # processing)
                                         patch_filter_by_area=args.patch_filter_by_area,
                                         # Amount of tissue that should
                                         # be present in a patch
                                         with_anno=with_anno,  # If true, you need to supply an additional XML file
                                         extract_layer=args.openslide_level  # OpenSlide Level
                                         )
        patch_extractor = PairwisePatchExtractor(tissue_detector, parameters, feature_map=fm, annotations=annotations)


        '''If num_processors is zero then multi processing is turned off'''
        if args.num_processors > 0:
            # Run the extraction process
            multiprocessing.set_start_method('spawn')
            pool = multiprocessing.Pool(processes=args.num_processors)
            pool.map(patch_extractor.extract, [args.wsi_fn, args.wsi_reg_2, offset])
        else:
            patch_num = patch_extractor.extract(args.wsi_fn, args.wsi_reg_2, offset)
    else :
        '''this block is called in patch_extraction  and in patch_extraction with image annotations'''
        parameters = ExtractorParameters(args.out_dir,               # Where the patches should be extracted to
                                         save_format=args.save_format,  # Can be '.jpg', '.png', or '.tfrecord'
                                         sample_cnt=args.sample_cnt,    # Limit the number of patches to extract
                                                                        # (-1 == all patches)
                                         patch_size=args.patch_size,    # Size of patches to extract (Height & Width)
                                         rescale_rate=args.rescale_rate,# Fold size to scale the thumbnail to (for faster \
                                                                        # processing)
                                         patch_filter_by_area=args.patch_filter_by_area,    # Amount of tissue that should
                                                                                            # be present in a patch
                                         with_anno=with_anno,           # If true, you need to supply an additional XML file
                                         extract_layer=args.openslide_level                 # OpenSlide Level
                                         )



        # Will be another step for Annotations here
        # Create the extractor object
        patch_extractor = PatchExtractor(tissue_detector,
                                         parameters,
                                         feature_map=fm,  # Need to update this when available
                                         annotations=annotations   # Need to update this when available
                                         )



        '''If num_processors is zero then multi processing is turned off'''
        if args.num_processors > 0:
            # Run the extraction process
            multiprocessing.set_start_method('spawn')
            pool = multiprocessing.Pool(processes=args.num_processors)
            pool.map(patch_extractor.extract, [args.wsi_fn])
        else:
            patch_num = patch_extractor.extract(args.wsi_fn)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
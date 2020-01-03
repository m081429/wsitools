from wsitools.tissue_detection.tissue_detector import TissueDetector
from wsitools.patch_extraction.patch_extractor import ExtractorParameters, PatchExtractor

wsi_fn = "/projects/shart/digital_pathology/scripts/DigiPath_MLTK_versions/DigiPath_MLTK/data/images/CMU-1-Small-Region.svs"
output_dir = "/projects/shart/digital_pathology/data/test/patches"

tissue_detector = TissueDetector("LAB_Threshold", threshold=85)
parameters = ExtractorParameters(output_dir, save_format='.png', sample_cnt=-1)
patch_extractor = PatchExtractor(tissue_detector, parameters, feature_map=None, annotations=None)
patch_num = patch_extractor.extract(wsi_fn)

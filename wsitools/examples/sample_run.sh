#export PYTHONPATH=$PYTHONPATH:/projects/shart/digital_pathology/scripts/wsitools/
input=/projects/shart/digital_pathology/scripts/DigiPath_MLTK_versions/DigiPath_MLTK/data/images/CMU-1-Small-Region.svs
output=/projects/shart/digital_pathology/data/test/patches
fm=/projects/shart/digital_pathology/scripts/wsitools/wsitools/patch_extraction/feature_maps/basic_fm_PL_eval.csv
#python /projects/shart/digital_pathology/scripts/wsitools/wsitools/wrappers/extract_patches.py -w $input -o $output -s 224 -m Patch_extraction -n 0 -F $fm -f .tfrecord
# -l 1
input=/projects/shart/digital_pathology/data/PenMarking/WSIs/MELF/e39a8d60a56844d695e9579bce8f0335.tiff
class_label_id_csv=/projects/shart/digital_pathology/scripts/wsitools/wsitools/wsi_annotation/examples/class_label_id.csv
xml_fn=/projects/shart/digital_pathology/scripts/wsitools/wsitools/wsi_annotation/examples/e39a8d60a56844d695e9579bce8f0335.xml
#python /projects/shart/digital_pathology/scripts/wsitools/wsitools/wrappers/extract_patches.py -w $input -o $output -s 224 -m Patch_extraction_with_ann -n 0 -F $fm -f .tfrecord -x $xml_fn -y $class_label_id_csv
#export PYTHONPATH=$PYTHONPATH:/projects/shart/digital_pathology/scripts/wsitools/
#####PATCH EXTRACTION#######
input=/projects/shart/digital_pathology/scripts/DigiPath_MLTK_versions/DigiPath_MLTK/data/images/CMU-1-Small-Region.svs
output=/projects/shart/digital_pathology/data/test/patches
fm=/projects/shart/digital_pathology/scripts/wsitools/wsitools/patch_extraction/feature_maps/basic_fm_PL_eval.csv
python /projects/shart/digital_pathology/scripts/wsitools/wsitools/wrappers/extract_patches.py -w $input -o $output -s 224 -n 0 -F $fm -f .tfrecord -l 1
#####PATCH EXTRACTION with ANNOTATIONS#######
input=/projects/shart/digital_pathology/data/PenMarking/WSIs/MELF/e39a8d60a56844d695e9579bce8f0335.tiff
class_label_id_csv=/projects/shart/digital_pathology/scripts/wsitools/wsitools/wsi_annotation/examples/class_label_id.csv
xml_fn=/projects/shart/digital_pathology/scripts/wsitools/wsitools/wsi_annotation/examples/e39a8d60a56844d695e9579bce8f0335.xml
#python /projects/shart/digital_pathology/scripts/wsitools/wsitools/wrappers/extract_patches.py -w $input -o $output -s 224  -n 0 -F $fm -f .tfrecord -x $xml_fn -y $class_label_id_csv
#####PATCH EXTRACTION with IMAGE REGISTRATION#######
float_input=/projects/shart/digital_pathology/data/PenMarking/WSIs/MELF-Clean/54742d6c5d704efa8f0814456453573a.tiff
off_set_x=-1620.95
off_set_y=1675.6
fm=/projects/shart/digital_pathology/scripts/wsitools/wsitools/patch_extraction/feature_maps/basic_fm_PPL_eval.csv
#python /projects/shart/digital_pathology/scripts/wsitools/wsitools/wrappers/extract_patches.py -w $input -o $output -s 224  -n 0 -F $fm -f .tfrecord -W $float_input -Ox $off_set_x -Oy $off_set_y
#####PATCH EXTRACTION with IMAGE REGISTRATION and with out offsetvalues#######
#python /projects/shart/digital_pathology/scripts/wsitools/wsitools/wrappers/extract_patches.py -w $input -o $output -s 224  -n 0 -F $fm -f .tfrecord -W $float_input
#####PATCH EXTRACTION with IMAGE REGISTRATION & ANNOTATION#######
#python /projects/shart/digital_pathology/scripts/wsitools/wsitools/wrappers/extract_patches.py -w $input -o $output -s 224 -n 0 -F $fm -f .tfrecord -W $float_input -Ox $off_set_x -Oy $off_set_y -x $xml_fn -y $class_label_id_csv
#####PATCH EXTRACTION with IMAGE REGISTRATION & ANNOTATION with out offset#######
#python /projects/shart/digital_pathology/scripts/wsitools/wsitools/wrappers/extract_patches.py -w $input -o $output -s 224 -n 0 -F $fm -f .tfrecord -W $float_input -x $xml_fn -y $class_label_id_csv

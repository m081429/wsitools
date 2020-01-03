#export PYTHONPATH=$PYTHONPATH:/projects/shart/digital_pathology/scripts/wsitools/
python /projects/shart/digital_pathology/scripts/wsitools/wsitools/wrappers/extract_patches.py -w /projects/shart/digital_pathology/scripts/DigiPath_MLTK_versions/DigiPath_MLTK/data/images/CMU-1-Small-Region.svs -o /projects/shart/digital_pathology/data/test/patches -s 224 -m Patch_extraction -n 0
# -l 1

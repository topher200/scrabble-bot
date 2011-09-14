./generate_input_file.py
./upload_to_s3.sh

datetime=$(date +"%Y%m%d-%T")
elastic-mapreduce --stream --enable-debugging \
--mapper s3://tophernet.scrabble/map.py \
--input s3://tophernet.scrabble/positions_to_try.txt \
--output s3://tophernet.scrabble.output/output_$datetime \
--reducer s3://tophernet.scrabble/reduce.py  \
--cache-archive s3://tophernet.scrabble/helper_classes.tar#helper_classes \
-j j-3BASVGYS0MIX8

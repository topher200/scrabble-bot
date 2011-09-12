./upload_to_s3.sh

elastic-mapreduce --stream \
--mapper s3://tophernet.scrabble/map.py \
--input s3://tophernet.scrabble/input.txt \
--output s3://tophernet.scrabble.output/output \
--reducer aggregate  \
--cache-archive s3://tophernet.scrabble/helper_classes.tar#helper_classes \
-j j-3BASVGYS0MIX8

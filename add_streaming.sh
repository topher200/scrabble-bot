./upload_to_s3.sh
elastic-mapreduce --stream --mapper s3://tophernet.scrabble/map.py --input s3://tophernet.scrabble/input.txt --output s3://tophernet.scrabble.output/out_1 --reducer s3://tophernet.scrabble/reduce.py  -j j-3BASVGYS0MIX8

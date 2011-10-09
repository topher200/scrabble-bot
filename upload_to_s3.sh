s3cmd sync positions_to_try.txt s3://tophernet.scrabble
s3cmd sync map.py s3://tophernet.scrabble
s3cmd sync reduce.py s3://tophernet.scrabble
find scrabble | grep -e txt -e py$ | awk -F '/' '{print $2}' | \
    xargs tar -C scrabble -cf scrabble.tar
s3cmd sync scrabble.tar s3://tophernet.scrabble

s3cmd sync positions_to_try.txt s3://tophernet.scrabble
s3cmd sync map.py s3://tophernet.scrabble
s3cmd sync reduce.py s3://tophernet.scrabble
tar -cf scrabble.tar scrabble/*
s3cmd sync scrabble.tar s3://tophernet.scrabble

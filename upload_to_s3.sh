s3cmd sync input.txt s3://tophernet.scrabble
s3cmd sync short_dictionary.txt s3://tophernet.scrabble
s3cmd sync dictionary.txt s3://tophernet.scrabble
s3cmd sync *.py s3://tophernet.scrabble
tar -cf helper_classes.tar helper_classes/*
s3cmd sync helper_classes.tar s3://tophernet.scrabble

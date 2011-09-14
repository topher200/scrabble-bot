s3cmd sync positions_to_try.txt s3://tophernet.scrabble
s3cmd sync map.py s3://tophernet.scrabble
s3cmd sync reduce.py s3://tophernet.scrabble
tar -cf helper_classes.tar position.py scrabble.py board.py __init__.py \
    short_dictionary.txt future_itertools.py
s3cmd sync helper_classes.tar s3://tophernet.scrabble

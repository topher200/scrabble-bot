#!/usr/bin/env python
import sys

def main(args):
  words = set()
  for word_list in args[1]:
    if type(word_list) == str:
      # Crap- it's not a list. It's just a single word
      words.add(word_list)
    else:
      assert type(word_list) == list
      # Add every word in the list
      for word in word_list:
        words.add(word)
  print words

if __name__ == '__main__':
  main(sys.argv)

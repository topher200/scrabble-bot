#!/usr/bin/env python
import sys

def main():
  words = set()
  for word in sys.stdin:
    words.add(word)
  print words

if __name__ == '__main__':
  main()

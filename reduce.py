#!/usr/bin/env python
import sys

def main():
  words = set()
  for word in sys.stdin:
    words.add(word.strip())
  for word in words:
    print word

if __name__ == '__main__':
  main()

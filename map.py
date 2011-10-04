#!/usr/bin/env python
from __future__ import print_function
import sys
sys.path.append('./helper_classes')  # necessary for Hadoop
import logging
import time
from position import PositionWithDirection
import scrabble

def main():
  positions_to_try = [PositionWithDirection.parse_from_string(line)
                      for line in sys.stdin]
  scrabble.main(positions_to_try, print)

if __name__ == '__main__':
  main()

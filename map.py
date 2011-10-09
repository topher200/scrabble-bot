#!/usr/bin/env python
import sys
sys.path.append('./helper_classes')  # necessary for Hadoop
import logging
import time
from position import PositionWithDirection
import scrabble

def main():
  positions_to_try = [PositionWithDirection.parse_from_string(line)
                      for line in sys.stdin]
  scrabble.main(positions_to_try, sys.stdout)

if __name__ == '__main__':
  main()

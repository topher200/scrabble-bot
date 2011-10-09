#!/usr/bin/env python
import sys
import logging
import time
import scrabble.game
from scrabble.position import PositionWithDirection

def main():
  positions_to_try = [PositionWithDirection.parse_from_string(line)
                      for line in sys.stdin]
  scrabble.game.main(positions_to_try, sys.stdout)

if __name__ == '__main__':
  main()

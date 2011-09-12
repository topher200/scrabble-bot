#!/usr/bin/env python
import sys
sys.path.append('./helper_classes')  # necessary for Hadoop
import logging
import time
from position import Position, PositionToTry
from scrabble import Scrabble

def set_up_game():
  game = Scrabble()

  game.board.add_letters('radar', Position(7, 4), Position.ACROSS)
  game.board.add_letters('oom', Position(8, 4), Position.DOWN)
  game.board.add_letters('eet', Position(10, 5), Position.ACROSS)
  game.board.add_letters('admie', Position(3, 8), Position.DOWN)

  return game

def main(args):
  start_time = time.time()

  game = set_up_game()
  position_to_try = PositionToTry()
  position_to_try.parse_from_string(args[1])

  print(game.try_letters_at_position([
        't', 'e', 'c', 
        ], position_to_try))

  end_time = time.time()
  logging.debug("script took %s minutes" % ((end_time - start_time) / 60))

if __name__ == '__main__':
  main(sys.argv)

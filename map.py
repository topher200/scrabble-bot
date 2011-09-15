#!/usr/bin/env python
import sys
sys.path.append('./helper_classes')  # necessary for Hadoop
import logging
import time
from position import Position, PositionWithDirection
from scrabble import Scrabble

def set_up_game():
  game = Scrabble()

  game.board.add_letters('sire', Position(7, 7), Position.ACROSS)
  game.board.add_letters('peheats', Position(6, 9), Position.DOWN)
  game.board.add_letters('jt', Position(10, 8), Position.ACROSS)
  game.board.add_letters('sidd', Position(8, 6), Position.ACROSS)
  game.board.add_letters('gri', Position(12, 6), Position.ACROSS)
  game.board.add_letters('ba', Position(10, 6), Position.DOWN)
  game.board.add_letters('ty', Position(10, 11), Position.ACROSS)

  return game

def main():
  start_time = time.time()

  for line in sys.stdin:
    game = set_up_game()
    position_to_try = PositionWithDirection()
    position_to_try.parse_from_string(line)

    logging.info('Running at position: %s' % str(position_to_try))
    word_list = game.try_letters_at_position([
        't', 'e', 'c', 
        ], position_to_try)
    for word in word_list:
      print word

  end_time = time.time()
  logging.info("script took %s minutes" % ((end_time - start_time) / 60))

if __name__ == '__main__':
  main()

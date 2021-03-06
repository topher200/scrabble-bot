#!/usr/bin/env python
from __future__ import division
from __future__ import with_statement
import future_itertools
import logging
import os
import sys
import time
from position import Position, PositionWithDirection, LettersAtPosition
from board import Board, OutOfBoundsException

# Set up dictionary. It is located in the same directory as this library.
DICTIONARY = set()
dir_path = os.path.dirname(os.path.abspath(__file__))
filename = 'dictionary.txt'
with open(os.path.join(dir_path, filename), 'r') as f:
  for word in f.readlines():
    DICTIONARY.add(word.strip())

class Scrabble:
  def __init__(self, rack):
    self.rack = rack
    self.board = Board()

  def is_word(self, possible_word):
    return (possible_word in DICTIONARY)

  def _try_letters_at_position(self, board, letters_at_position):
    '''Adds the letters to the board at the given position. Returns False if a
    non-word is created by any letter.'''
    starting_pos = letters_at_position.position_with_direction.position.copy()
    direction = letters_at_position.position_with_direction.direction
    letters = letters_at_position.letters
    try:
      board.add_letters(letters, starting_pos, direction)
    except OutOfBoundsException:
      return False
    # Check that there is a word at the original position/direction
    if not self.is_word(board.get_word(starting_pos, direction)):
      # We didn't make a real word
      return False
    # We made a real word, now check to make sure we didn't create any
    # non-words in the other direction.
    other_direction = Position.get_other_direction(direction)
    moving_position = starting_pos.copy()
    for _ in range(len(letters)):
      generated_word = board.get_word(moving_position, other_direction)
      moving_position.add_in_direction(1, direction)  # for next time
      if len(generated_word) < 2:
        # This one isn't a word- it's just a letter. We're fine
        continue
      if not self.is_word(generated_word):
        # We accidentally made a non word!
        return False
    # We made a word, and didn't make any non-words in the other direction!
    return True

  def try_rack_at_position(self, position_to_try):
    '''Try all combinations of the rack letters at position to see if we can
    make a word. The minimum word length is the distance to the closest
    letter, to make sure we're touching it.'''
    good_words = []
    minimum_num_letters = self.board.get_spaces_to_next_letter(position_to_try)
    for num_letters in range(minimum_num_letters, 8):
      for letters_to_try in future_itertools.permutations(self.rack,
                                                          num_letters):
        # Make a fake board and add these letters to it
        temp_board = self.board.copy()
        letters_at_position = LettersAtPosition(position_to_try,
                                                letters_to_try)
        try:
          if self._try_letters_at_position(temp_board, letters_at_position):
            # We made a word!
            good_words.append(letters_at_position)
        except OutOfBoundsException:
          # Just skip if we start or end out of bounds
          continue
    return good_words

  def generate_positions_to_try(self, ):
    '''Returns all possible places where our 7 letters could be played. This
    means the 7 spaces to the top/left of each piece on the board, and 1 space
    to the down/right. A position is skipped if it is not on the board or
    already occupied by a piece.

    Return type is PositionWithDirection, which gives the position and
    direction to be tried.'''
    positions_to_try = set()
    for base_position in self.board.get_position_of_all_letters():
      for direction in Position.DIRECTIONS:
        # Try 7 to the left (or up), and 1 to the right (or down)
        magnitudes_to_try = range(-7, 0) + [1]
        for distance_away_from_base in magnitudes_to_try:
          position = base_position.copy()
          position.add_in_direction(distance_away_from_base, direction)
          if self.board.position_is_out_of_bounds(position):
            # Can't start at an out of bounds position
            continue
          if not self.board.is_blank(position):
            # Skipping position- already has a letter
            continue
          positions_to_try.add(PositionWithDirection(position, direction))
    return positions_to_try


def set_up_game():
  rack = [
    'q', 'i', 's', 'n', 'e', 'c', 'n', 
    ]
  game = Scrabble(rack)
  game.board.add_letters('painter', Position(7, 7), Position.DOWN)
  game.board.add_letters('dogaped', Position(10, 4), Position.ACROSS)
  game.board.add_letters('avent', Position(9, 4), Position.DOWN)
  game.board.add_letters('aragon', Position(7, 7), Position.ACROSS)
  game.board.add_letters('yow', Position(8, 10), Position.ACROSS)
  game.board.add_letters('maw', Position(6, 10), Position.ACROSS)
  game.board.add_letters('m', Position(9, 4), Position.ACROSS)
  game.board.add_letters('ooz', Position(12, 1), Position.ACROSS)
  game.board.add_letters('fecil', Position(3, 8), Position.DOWN)
  game.board.add_letters('yagi', Position(0, 7), Position.DOWN)
  game.board.add_letters('blott', Position(0, 2), Position.ACROSS)
  game.board.add_letters('ex', Position(13, 8), Position.ACROSS)
  game.board.add_letters('glers', Position(1, 4), Position.DOWN)
  game.board.add_letters('deai', Position(4, 0), Position.ACROSS)
  game.board.add_letters('htik', Position(5, 4), Position.ACROSS)
  game.board.add_letters('rid', Position(14, 8), Position.ACROSS)
  game.board.add_letters('eated', Position(11, 8), Position.ACROSS)
  game.board.add_letters('un', Position(1, 2), Position.DOWN)
  game.board.add_letters('nins', Position(1, 1), Position.DOWN)
  game.board.add_letters('fur', Position(7, 3), Position.DOWN)

  return game


def main(positions_to_try=None):
  start_time = time.time()

  if positions_to_try == None:
    game = set_up_game()
    logging.warning(game.board)
    positions_to_try = game.generate_positions_to_try()

  for position_to_try in positions_to_try:
    logging.warn('Running at position: %s' % str(position_to_try))
    game = set_up_game()
    word_list = game.try_rack_at_position(position_to_try)
    for word_at_position in word_list:
      sys.stdout.write(str(word_at_position) + '\n')

  end_time = time.time()
  logging.warning("script took %s minutes" % ((end_time - start_time) / 60))

if __name__ == '__main__':
  main()

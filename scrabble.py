from __future__ import division
from __future__ import with_statement
import future_itertools
import logging
import os
import time
from position import Position, PositionWithDirection, LettersAtPosition
from board import Board, OutOfBoundsException

# Set up dictionary. Its location differs if running on local or Hadoop.
filename = 'dictionary.txt'
DICTIONARY = set()
try:
  f = open(filename, 'r')
# TODO(topher): is this necessary? shouldn't adding the helper directory
# to our path make it visiable in the script?
except IOError:
  f = open(os.path.join('helper_classes', filename), 'r')
for word in f.readlines():
  DICTIONARY.add(word.strip())
f.close()

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
    for _ in range(len(letters)):
      if not self.is_word(board.get_word(starting_pos, other_direction)):
        return False
      starting_pos.add_in_direction(1, direction)
    # We made a word, and didn't make any non-words in the other direction!
    return True

  def try_rack_at_position(self, position_to_try):
    '''Try all combinations of the rack letters at position to see if we can
    make a word. The minimum word length is the distance to the closest
    letter, to make sure we're touching it.'''
    good_words = []
    for num_letters in range(position_to_try.distance_to_closest_letter, 8):
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

    The return type is a dict of elements of the form:
    (Position, distance away from closest letter on board)'''
    positions_to_try = []
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
          positions_to_try.append(
            PositionWithDirection(position, direction,
                                  abs(distance_away_from_base)))
    return positions_to_try


def set_up_game():
  rack = [
    'v', 'e', 't', 'n', 'r', 'o', 't', 
    ]
  game = Scrabble(rack)
  game.board.add_letters('pain', Position(7, 7), Position.DOWN)

  return game


def main(positions_to_try=None, output=None):
  start_time = time.time()

  if positions_to_try == None:
    game = set_up_game()
    logging.warning(game.board)
    positions_to_try = game.generate_positions_to_try()
  if output == None:
    output = logging.fatal

  for position_to_try in positions_to_try:
    game = set_up_game()
    word_list = game.try_rack_at_position(position_to_try)
    for word_at_position in word_list:
      output(word_at_position)

  end_time = time.time()
  logging.warning("script took %s minutes" % ((end_time - start_time) / 60))

if __name__ == '__main__':
  main()

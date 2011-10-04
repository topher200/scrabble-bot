from __future__ import division
from __future__ import with_statement
import future_itertools
import logging
import os
import time
from position import Position, PositionWithDirection, LettersAtPosition
from board import Board, OutOfBoundsException

class Scrabble:
  def __init__(self, ):
    self.board = Board()

    # Set up dictionary. Its location differs if running on local or Hadoop.
    filename = 'dictionary.txt'
    self.dictionary = set()
    try:
      f = open(filename, 'r')
    # TODO(topher): is this necessary? shouldn't adding the helper directory
    # to our path make it visiable in the script?
    except IOError:
      f = open(os.path.join('helper_classes', filename), 'r')
    for word in f.readlines():
      self.dictionary.add(word.strip())
    f.close()

  def is_word(self, possible_word):
    return (possible_word in self.dictionary)

  # TODO(topher): needs a better name
  def try_letters(self, board, letters_at_position):
    '''Adds the letters to the board. Returns False if a non-word is created
    by any letter.'''
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

  def try_letters_at_position(self, letters, position_to_try):
    '''Try all combinations of the letters at position to see if we can make a
    word. The minimum word length is the distance to the closest letter, to
    make sure we're touching it.'''
    good_words = []
    for num_letters in range(position_to_try.distance_to_closest_letter, 8):
      for letters_to_try in future_itertools.permutations(letters, num_letters):
        # Make a fake board and add these letters to it
        temp_board = self.board.copy()
        letters_at_position = LettersAtPosition(position_to_try,
                                                letters_to_try)
        try:
          if self.try_letters(temp_board, letters_at_position):
            # We made a word!
            good_words.append(letters_at_position)
        except OutOfBoundsException:
          # Just skip if we start or end out of bounds
          continue
    return good_words

  def try_letters_at_positions_to_try(self, letters, positions_to_try):
    word_lists = []
    for position_to_try in positions_to_try:
      logging.info('trying position: %s' % position_to_try.position)
      word_lists.append(
        self.try_letters_at_position(letters, position_to_try))
    return word_lists

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

  def get_possible_words(self, letters, positions_to_try):
    '''Returns a list of the unique words we found.'''
    word_lists = self.try_letters_at_positions_to_try(letters, positions_to_try)
    words = []
    for word_list in word_lists:
      for word_at_position in word_list:
        words.append(word_at_position)
    return words

def main():
  start_time = time.time()

  game = Scrabble()
  game.board.add_letters('sire', Position(7, 7), Position.ACROSS)
  game.board.add_letters('peheats', Position(6, 9), Position.DOWN)
  game.board.add_letters('jt', Position(10, 8), Position.ACROSS)
  game.board.add_letters('sidd', Position(8, 6), Position.ACROSS)
  game.board.add_letters('gri', Position(12, 6), Position.ACROSS)
  game.board.add_letters('ba', Position(10, 6), Position.DOWN)
  game.board.add_letters('ty', Position(10, 11), Position.ACROSS)
  logging.warning(game.board)

  positions_to_try = game.generate_positions_to_try()
  word_list = game.get_possible_words([
      's', 'a', 't', 
        ], positions_to_try)
  for word_at_position in word_list:
    logging.fatal(word_at_position)

  end_time = time.time()
  logging.warning("script took %s minutes" % ((end_time - start_time) / 60))

if __name__ == '__main__':
  main()

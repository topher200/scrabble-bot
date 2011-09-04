from __future__ import division
from __future__ import with_statement
import itertools
import time
from position import Position
from board import Board

# Init dictionary
DICTIONARY = []
with open('short_dictionary.txt', 'r') as f:
  for word in f.readlines():
    DICTIONARY.append(word.strip())

class OutOfBoundsException(Exception):
  pass

class Scrabble:
  def __init__(self, board):
    self.board = board

  def try_letters_at_position(self, letters, position, direction,
                              minimum_num_of_letters):
    '''Try each combination (1 to minimum_num_of_letters letters) and see if
    it makes a word.'''
    words = []
    for num_letters in range(minimum_num_of_letters, 8):
      for potential_word in itertools.permutations(letters, num_letters):
        # Make a fake board and add these letters to it
        temp_board = self.board.copy()
        try:
          temp_board.add_letters(potential_word, position, direction)
        except OutOfBoundsException:
          # Just skip if we start or end out of bounds
          continue
        word = temp_board.get_word(position, direction)
        if word in DICTIONARY:
          # We made a word!
          words.append(word)
    return words

  def generate_positions_to_try(self, ):
    '''Returns all possible places where our 7 letters could be played. This
    means the 7 spaces to the top/left of each piece on the board, and 1 space
    to the down/right. A position is skipped if it is not on the board or
    already occupied by a piece.

    The return type is a dict of elements of the form:
    (Position, distance away from closest letter on board)'''
    position_dict = {}
    for base_position in self.board.get_position_of_all_letters():
      for direction in Position.DIRECTIONS:
        # Try 7 to the left (or up), and 1 to the right (or down)
        magnitudes_to_try = range(-7, 0) + [1]
        for distance_away_from_position in magnitudes_to_try:
          position = base_position.copy()
          position.add_in_direction(distance_away_from_position, direction)
          if self.board.position_is_out_of_bounds(position):
            # Can't start at an out of bounds position
            continue
          if not self.board.is_blank(position):
            # Skipping position- already has a letter
            continue
          if position_dict.get(position):
            # There's already a distance! Take the closer one.
            position_dict[position] = min(position_dict[position],
                                          abs(distance_away_from_position))
          else:
            # There's nothing yet- add our position
            position_dict[position] = abs(distance_away_from_position)
    return position_dict

  def try_letters_everywhere(self, letters, ):
    '''Attempt to use these letters anywhere they would work on the
    board. This means the 7 spaces to the top/left of each piece on the board,
    and 1 space to the down/right.

    Skips checking the position if it's already occupied by a letter.'''
    words = []
    for base_position in self.board.get_position_of_all_letters():
      for direction in Position.DIRECTIONS:
        # Try 7 to the left (or up), and 1 to the right (or down)
        magnitudes_to_try = range(-7, 0) + [1]
        for distance_away_from_position in magnitudes_to_try:
          position = base_position.copy()
          position.add_in_direction(distance_away_from_position, direction)
          if self.board.position_is_out_of_bounds(position):
            # Can't start at an out of bounds position
            continue
          if not self.board.is_blank(position):
            # Skipping position- already has a letter
            continue
          print 'position: %s' % position
          words.append(self.try_letters_at_position(
              letters, position, direction, abs(distance_away_from_position)))
    return words

  def get_possible_words(self, letters):
    '''Returns a list of the unique words we found.'''
    word_lists = self.try_letters_everywhere(letters)
    words = set()
    for word_list in word_lists:
      if type(word_list) == str:
        # Crap- it's not a list. It's just a single word
        words.add(word_list)
      for word in word_list:
        words.add(word)
    return words

def main():
  start_time = time.time()

  board = Board()
  game = Scrabble(board)
  game.board.add_letters('radar', Position(7, 4), Position.ACROSS)
  game.board.add_letters('oom', Position(8, 4), Position.DOWN)
  game.board.add_letters('eet', Position(10, 5), Position.ACROSS)
  game.board.add_letters('admie', Position(3, 8), Position.DOWN)
  print(game.board)

  print(game.get_possible_words([
        't', 'e', 'c', 
        ]))

  end_time = time.time()
  print("script took %s minutes" % ((end_time - start_time) / 60))

if __name__ == '__main__':
  main()

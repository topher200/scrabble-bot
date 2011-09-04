from __future__ import with_statement
import itertools
import numpy as np
import time
EMPTY = '.'

# Init dictionary
DICTIONARY = []
with open('short_dictionary.txt', 'r') as f:
  for word in f.readlines():
    DICTIONARY.append(word.strip())

class OutOfBoundsException(Exception):
  pass

class Board:
  BOARD_SIZE = 15
  def __init__(self, ):
    self.board =  np.zeros((self.BOARD_SIZE, self.BOARD_SIZE), 'string')
    # TODO: find a better way to initialize to spaces
    for x in range(len(self.board)):
      for y in range(len(self.board[x])):
        self.board[x,y] = EMPTY

  def is_blank(self, position):
    # Returns True if the block is empty
    if self[position] == EMPTY:
      return True
    return False

  def position_is_out_of_bounds(self, position):
    return (position.down < 0 or position.down >= self.BOARD_SIZE) or \
        (position.across < 0 or position.across >= self.BOARD_SIZE)

  def __getitem__(self, position):
    return self.board[position.down, position.across]

  def __setitem__(self, position, letter):
    self.board[position.down, position.across] = letter

  def __str__(self):
    string = ' 012345678901234\n'
    for x in range(len(self.board)):
      string += str(x % 10)
      for y in range(len(self.board[x])):
        string += self.board[x,y]
      string += '\n'
    return string

  def copy(self):
    new_board = Board()
    new_board.board = self.board.copy()
    return new_board

  def add_letters(self, letters, starting_position, direction):
    '''Put letters on each blank space on the board, starting at
    starting_position and moving in direction until all the letters are used
    up.'''
    position = starting_position.copy()
    while len(letters) > 0:
      if self.position_is_out_of_bounds(position):
        raise OutOfBoundsException("trying to add a letter OOB")
      if self.is_blank(position):
        # There's nothing here- put a letter down
        self[position] = letters[0]
        letters = letters[1:]
      # Move to the next position
      position.add_in_direction(1, direction)

  def get_word(self, position, direction):
    def get_before_blank(starting_position, direction, travel_direction):
      '''Returns the position of the last char before a blank (or edge of
      board). Moves along direction (DOWN, ACROSS) in travel_direction
      (left/up/-1 or down/across/+1).'''
      assert(not self.is_blank(starting_position))
      position = starting_position.copy()
      while not (self.position_is_out_of_bounds(position) or
                 self.is_blank(position)):
        position.add_in_direction(travel_direction, direction)
      # We have the position of the blank/edge! Back up 1.
      position.add_in_direction(-travel_direction, direction)
      return position

    position = get_before_blank(position, direction, -1)
    end = get_before_blank(position, direction, +1)
    word = self[position]
    while not position.equals(end):
      position.add_in_direction(1, direction)
      word += self[position]
    return word

  def get_position_of_letters_on_board(self,):
    '''Returns a Position for each letter currently placed on the board'''
    position_list = []
    for x in range(len(self.board)):
      for y in range(len(self.board[0])):
        position = Position(x, y)
        if not self.is_blank(position):
          position_list.append(position)
    return position_list

  def try_letters_at_position(self, letters, position, direction,
                              minimum_num_of_letters):
    '''Try each combination (1 to minimum_num_of_letters letters) and see if
    it makes a word.'''
    words = []
    for num_letters in range(minimum_num_of_letters, 8):
      for potential_word in itertools.permutations(letters, num_letters):
        # Make a fake board and add these letters to it
        temp_board = self.copy()
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

  def try_letters_everywhere(self, letters, ):
    '''Attempt to use these letters anywhere they would work on the
    board. This means the 7 spaces to the top/left of each piece on the board,
    and 1 space to the down/right.

    Skips checking the position if it's already occupied by a letter.'''
    words = []
    for base_position in self.get_position_of_letters_on_board():
      for direction in DIRECTIONS:
        # Try 7 to the left (or up), and 1 to the right (or down)
        magnitudes_to_try = range(-7, 0) + [1]
        for distance_away_from_position in magnitudes_to_try:
          position = base_position.copy()
          position.add_in_direction(distance_away_from_position, direction)
          if self.position_is_out_of_bounds(position):
            # Can't start at an out of bounds position
            continue
          if not self.is_blank(position):
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

DOWN = 0
ACROSS = 1
DIRECTIONS = [DOWN, ACROSS]
class Position():
  def __init__(self, down, across):
    self.down = down
    self.across = across

  def __str__(self, ):
    return '(%i, %i)' % (self.down, self.across)

  def equals (self, other_pos):
    return ((self.down == other_pos.down) and (self.across == other_pos.across))

  # TODO(topher): better way to create a copy
  def copy(self, ):
    return Position(self.down, self.across)

  def add_in_direction(self, magnitude, direction):
    if direction == ACROSS:
      self.across += magnitude
    elif direction == DOWN:
      self.down += magnitude
    else:
      raise Exception("shouldn't get here. Direction: %s" % direction)

def main():
  start_time = time.time()

  board = Board()
  board.add_letters('radar', Position(7, 5), ACROSS)
  board.add_letters('room', Position(7, 5), DOWN)
  print(board)

  print(board.get_possible_words([
        't', 'e', 'a', 
        ]))

  end_time = time.time()
  print("script took %s seconds" % (end_time - start_time))

if __name__ == '__main__':
  main()

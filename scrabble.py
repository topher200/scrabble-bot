from __future__ import with_statement
import itertools
import numpy as np
EMPTY = '.'

# Init dictionary
DICTIONARY = []
with open('short_dictionary.txt', 'r') as f:
  for word in f.readlines():
    DICTIONARY.append(word.strip())

class Board:
  BOARD_SIZE = 15
  def __init__(self, ):
    self.board =  np.zeros((self.BOARD_SIZE, self.BOARD_SIZE), 'string')
    # TODO: find a better way to initialize to spaces
    for x in range(len(self.board)):
      for y in range(len(self.board[x])):
        self.board[x,y] = EMPTY

  def is_blank(self, position):
    # Returns True if the block is empty or out of bounds.
    if self.position_is_out_of_bounds(position_is_out_of_bounds):
      return True
    if self[position] == EMPTY:
      return True
    return False

  def position_is_out_of_bounds(self, position):
    return (position.down < 0 or position.down >= BOARD_SIZE) or \
        (position.across < 0 or position.across >= BOARD_SIZE)

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
    position = starting_position.copy()
    while len(letters) > 0:
      # Put down a letter if there's nothing here
      if self[position] == EMPTY:
       self[position] = letters[0]
       letters = letters[1:]
      if direction == ACROSS:
        position.across += 1
      else:
        position.down += 1

  def get_word(self, position, direction):
    def get_before_blank(starting_position, direction, travel_direction):
      # returns the position of the last char before a blank
      assert(not self.is_blank(starting_position))
      position = starting_position.copy()
      while not self.is_blank(position):
        if direction == ACROSS:
          position.across += travel_direction
        else:
          position.down += travel_direction
      # We have the position of the blank! Back up 1
      if direction == ACROSS:
        position.across -= travel_direction
      else:
        position.down -= travel_direction
      return position

    start = get_before_blank(position, direction, -1)
    end = get_before_blank(position, direction, +1)
    word = self[start]
    while not start.equals(end):
      if direction == ACROSS:
        start.across += 1
      else:
        start.down += 1
      word += self[start]
    return word

  def get_position_of_letters_on_board(self,):
    position_list = []
    for x in range(len(self.board)):
      for y in range(len(self.board[0])):
        letter = self.board[x, y]
        if letter != EMPTY:
          position_list.append(Position(x, y))
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
        temp_board.add_letters(potential_word, position, direction)
        word = temp_board.get_word(position, direction)
        if word in DICTIONARY:
          # We made a word!
          words.append(word)
    return words

  def try_letters_everywhere(self, letters, ):
    '''Attempt to use these letters anywhere they would work on the
    board. This means the 7 spaces to the top/left of each piece on the board,
    and 1 space to the down/right.'''
    words = []
    for base_position in self.get_position_of_letters_on_board():
      for direction in DIRECTIONS:
        # Try 7 to the left (or up), and 1 to the right (or down)
        magnitudes_to_try = range(-7, 0) + [1]
        for distance_away_from_position in magnitudes_to_try:
          position = base_position.copy()
          position.add_in_direction(distance_away_from_position, direction)
          words.append(self.try_letters_at_position(
              letters, position, direction, abs(distance_away_from_position)))
          print position, words[-1]
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

board = Board()
board.add_letters('asdf', Position(7, 5), ACROSS)
board.add_letters('qwerty', Position(6, 8), DOWN)
print(board.get_word(Position(7,7), ACROSS))
print(board.try_letters_at_position(['c', 'o', 'g', 'a', 'b',],
                                    Position(6,7), DOWN, 1))

print(board)

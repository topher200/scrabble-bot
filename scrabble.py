from __future__ import with_statement
import itertools
import numpy as np
EMPTY = '.'

class Board:
  BOARD_SIZE = 15
  def __init__(self, ):
    self.board =  np.zeros((self.BOARD_SIZE, self.BOARD_SIZE), 'string')
    # TODO: find a better way to initialize to spaces
    for x in range(len(self.board)):
      for y in range(len(self.board[x])):
        self.board[x,y] = EMPTY

  def is_blank(self, position):
    # Try to check for blank. If we get an exception, we know we're out of bounds
    # TODO(topher): add OOB error case
    if self[position] == EMPTY:
      return True
    return False

  def __getitem__(self, position):
    return self.board[position.down, position.across]

  def __setitem__(self, position, letter):
    self.board[position.down, position.across] = letter

  def __str__(self):
    str = ''
    for x in range(len(self.board)):
      for y in range(len(self.board[x])):
        str += self.board[x,y]
      str += '\n'
    return str

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

  def try_letters(self, letters, position, direction, minimum_num_of_letters):
    words = []
    for num_letters in range(minimum_num_of_letters, 8):
      for letter_combination in itertools.permutations(letters, num_letters):
        temp_board = self.copy()
        temp_board.add_letters(letter_combination, position, direction)
        # TODO
        # check if we made a word
        #   save if we did
        # ignores words up/down we may have made
    return words
  

# Init dictionary
dictionary = []
with open('dictionary.txt', 'r') as f:
  for word in f.readlines():
    dictionary.append(word.strip())

DOWN = 0
ACROSS = 1
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

board = Board()
board.add_letters('asdf', Position(7, 5), ACROSS)
print(board.get_word(Position(7,7), ACROSS))
print(board.try_letters(['a', 'b',], Position(6,6), DOWN, 1))

print(board)

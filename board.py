import numpy as np
from position import Position

EMPTY_SPACE = '.'

class Board:
  BOARD_SIZE = 15
  def __init__(self, ):
    self.spaces =  np.zeros((self.BOARD_SIZE, self.BOARD_SIZE), 'string')
    # TODO: find a better way to initialize to spaces
    for x in range(len(self.spaces)):
      for y in range(len(self.spaces[x])):
        self.spaces[x,y] = EMPTY_SPACE

  def is_blank(self, position):
    # Returns True if the block is empty
    if self[position] == EMPTY_SPACE:
      return True
    return False

  def position_is_out_of_bounds(self, position):
    return (position.down < 0 or position.down >= self.BOARD_SIZE) or \
        (position.across < 0 or position.across >= self.BOARD_SIZE)

  def __getitem__(self, position):
    return self.spaces[position.down, position.across]

  def __setitem__(self, position, letter):
    self.spaces[position.down, position.across] = letter

  def __str__(self):
    string = ' 012345678901234\n'
    for x in range(len(self.spaces)):
      string += str(x % 10)
      for y in range(len(self.spaces[x])):
        string += self.spaces[x,y]
      string += '\n'
    return string

  def copy(self):
    new_board = Board()
    new_board.spaces = self.spaces.copy()
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
    while position != end:
      position.add_in_direction(1, direction)
      word += self[position]
    return word

  def get_position_of_all_letters(self,):
    '''Returns a Position for each letter currently placed on the board'''
    position_list = []
    for x in range(len(self.spaces)):
      for y in range(len(self.spaces[0])):
        position = Position(x, y)
        if not self.is_blank(position):
          position_list.append(position)
    return position_list


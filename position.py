class Position(object):
  DOWN = 0
  ACROSS = 1
  DIRECTIONS = [DOWN, ACROSS]

  def __init__(self, down, across):
    self.down = down
    self.across = across

  def __str__(self, ):
    return '(%i, %i)' % (self.down, self.across)

  def __eq__(self, other_pos):
    return ((self.down == other_pos.down) and (self.across == other_pos.across))

  def __ne__(self, other_pos):
    return not (self == other_pos)

  def __hash__(self, ):
    return int('%03i%03i' %(self.down, self.across))

  # TODO(topher): better way to create a copy
  def copy(self, ):
    return Position(self.down, self.across)

  def add_in_direction(self, magnitude, direction):
    if direction == Position.ACROSS:
      self.across += magnitude
    elif direction == Position.DOWN:
      self.down += magnitude
    else:
      raise Exception("shouldn't get here. Direction: %s" % direction)


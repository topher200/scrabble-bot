import re

class Position(object):
  DOWN = 0
  ACROSS = 1
  DIRECTIONS = [DOWN, ACROSS]

  def __init__(self, down = 0, across = 0):
    self.down = down
    self.across = across

  def __eq__(self, other_pos):
    return ((self.down == other_pos.down) and (self.across == other_pos.across))

  def __ne__(self, other_pos):
    return not (self == other_pos)

  def __hash__(self, ):
    return int('%03i%03i' %(self.down, self.across))

  def __str__(self, ):
    return '(%i, %i)' % (self.down, self.across)

  def parse_from_string(self, string):
    (self.down, self.across) = \
        map(int, re.search('(\d+), (\d+)', string).groups())

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
    
class PositionWithDirection(object):
  def __init__(self, position = Position(), direction = Position.ACROSS,
               distance_to_closest_letter = 1):
    self.position = position
    self.direction = direction
    self.distance_to_closest_letter = distance_to_closest_letter

  def __str__(self, ):
    return('pos:%s, direction:%i, min_distance:%i' % \
        (str(self.position), self.direction, self.distance_to_closest_letter))

  def __eq__(self, other_ptt):
    return (self.position == other_ptt.position) and \
        (self.direction == other_ptt.direction) and \
        (self.distance_to_closest_letter == \
           other_ptt.distance_to_closest_letter)

  def parse_from_string(self, string):
    match = re.match('pos:(.*), direction:(\d+), min_distance:(\d+)', string)
    self.position.parse_from_string(match.group(1))
    self.direction = int(match.group(2))
    self.distance_to_closest_letter = int(match.group(3))


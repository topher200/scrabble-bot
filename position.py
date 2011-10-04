import re

class Position(object):
  DOWN = 0
  ACROSS = 1
  DIRECTIONS = [DOWN, ACROSS]

  def __init__(self, down, across):
    self.down = down
    self.across = across

  @classmethod
  def parse_from_string(cls, string):
    down, across = map(int, re.search('(\d+), (\d+)', string).groups())
    return cls(down, across)

  def __eq__(self, other_pos):
    return ((self.down == other_pos.down) and (self.across == other_pos.across))

  def __ne__(self, other_pos):
    return not (self == other_pos)

  def __hash__(self, ):
    return int('%03i%03i' %(self.down, self.across))

  def __str__(self, ):
    return '(%i, %i)' % (self.down, self.across)

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

  @staticmethod
  def get_other_direction(direction):
    if direction == Position.DOWN:
      return Position.ACROSS
    else:
      return Position.DOWN

    
class PositionWithDirection(object):
  def __init__(self, position, direction, distance_to_closest_letter = 1):
    self.position = position
    self.direction = direction
    self.distance_to_closest_letter = distance_to_closest_letter

  @classmethod
  def parse_from_string(cls, string):
    match = re.match('pos:(.*), direction:(\d+), min_distance:(\d+)', string)
    position = Position.parse_from_string(match.group(1))
    direction = int(match.group(2))
    distance_to_closest_letter = int(match.group(3))
    return cls(position, direction, distance_to_closest_letter)

  def __str__(self, ):
    return('pos:%s, direction:%i, min_distance:%i' % \
        (str(self.position), self.direction, self.distance_to_closest_letter))

  def __eq__(self, other_ptt):
    return (self.position == other_ptt.position) and \
        (self.direction == other_ptt.direction) and \
        (self.distance_to_closest_letter == \
           other_ptt.distance_to_closest_letter)


class LettersAtPosition:
  def __init__(self, position_with_direction, letters):
    self.position_with_direction = position_with_direction
    self.letters = letters

  @classmethod
  def parse_from_string(cls, string):
    match = re.match('letters: {(.*)} at position: {(.*)}', string)
    position_with_direction = \
        PositionWithDirection.parse_from_string(match.group(2))
    import string
    # Grab every char in the letters 'group'
    letters = [char for char in match.group(1) \
                 if char in string.ascii_lowercase]
    return cls(position_with_direction, letters)

  def __str__(self, ):
    return ('letters: {%s} at position: {%s}' %
            (self.letters, self.position_with_direction))

  def __eq__(self, other_lap):
    return (self.position_with_direction == \
              other_lap.position_with_direction) and \
              (self.letters == other_lap.letters)

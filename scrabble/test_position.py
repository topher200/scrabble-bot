import unittest
from position import Position, PositionWithDirection, LettersAtPosition

class PositionTest(unittest.TestCase):
  def test_parse_from_string(self, ):
    orig = Position(14, 12)
    new = Position.parse_from_string(str(orig))
    self.assertEqual(orig, new)

class PositionWithDirectionTest(unittest.TestCase):
  def test_parse_from_string(self):
    orig = PositionWithDirection(Position(10, 15), Position.DOWN)
    new = PositionWithDirection.parse_from_string(str(orig))
    self.assertEqual(orig, new)

class LettersAtPositionTest(unittest.TestCase):
  @staticmethod
  def _create_letters_at_position():
    return LettersAtPosition(PositionWithDirection(Position(6, 7),
                                                   Position.DOWN),
                             ['a', 'b', 'c'])

  def test_equality(self):
    orig = self._create_letters_at_position()
    new = self._create_letters_at_position()
    self.assertEqual(orig, new)

  def test_parse_from_string(self):
    orig = self._create_letters_at_position()
    new = LettersAtPosition.parse_from_string(str(orig))
    self.assertEqual(orig, new)

if __name__ == '__main__':
  unittest.main()


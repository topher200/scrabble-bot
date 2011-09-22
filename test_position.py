import unittest
from position import Position, PositionWithDirection

class PositionTest(unittest.TestCase):
  def test_parse_from_string(self, ):
    orig = Position(14, 12)
    new = Position()
    new.parse_from_string(str(orig))
    self.assertEqual(orig, new)

class PositionWithDirectionTest(unittest.TestCase):
  def test_parse_from_string(self):
    orig = PositionWithDirection(Position(10, 15), Position.DOWN, 5)
    new = PositionWithDirection.parse_from_string(str(orig))
    self.assertEqual(orig, new)

if __name__ == '__main__':
  unittest.main()


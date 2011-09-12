import unittest
from position import Position, PositionToTry

class PositionTest(unittest.TestCase):
  def test_parse_from_string(self, ):
    orig = Position(14, 12)
    new = Position()
    new.parse_from_string(str(orig))
    self.assertEqual(orig, new)

class PositionToTryTest(unittest.TestCase):
  def test_parse_from_string(self):
    orig = PositionToTry(Position(10, 15), Position.DOWN, 5)
    new = PositionToTry()
    new.parse_from_string(str(orig))
    self.assertEqual(orig, new)

if __name__ == '__main__':
  unittest.main()

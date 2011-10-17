#!/usr/bin/env python
from scrabble.position import LettersAtPosition
import scrabble.game
import string
import sys

def view(moves=None):
  if moves == None:
    moves = sys.stdin

  for position_to_view in moves:
    game = scrabble.game.set_up_game()
    pos = LettersAtPosition.parse_from_string(position_to_view)
    if len(pos.letters) < 5:
      continue
    game.board.add_letters(map(string.upper, pos.letters),
                           pos.position_with_direction.position,
                           pos.position_with_direction.direction)
    for letter in pos.letters:
      print letter,
    print game.board
    print '\n'


if __name__ == '__main__':
  view()

#!/usr/bin/env python
from __future__ import with_statement
import scrabble.game

game = scrabble.game.set_up_game()
filename = 'positions_to_try.txt'
with open(filename, 'w') as file:
  for ptt in game.generate_positions_to_try():
    file.write(str(ptt) + '\n')



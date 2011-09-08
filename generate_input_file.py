from __future__ import with_statement
import map

game = map.set_up_game()
filename = 'input.txt'
with open(filename, 'w') as file:
  for ptt in game.generate_positions_to_try():
    file.write(str(ptt) + '\n')



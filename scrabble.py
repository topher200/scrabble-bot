from __future__ import with_statement
import numpy
letters_in_hand = [
  'n', 'i', 'a', 'p', 'g', 'i', 
  ]
global_letters = [
  'z', 'b', 'r', 'o', 's', 'l', 'w',
  ]

def load_dictionary():
  dictionary = []
  with open('dictionary.txt', 'r') as f:
    for word in f.readlines():
      dictionary.append(word.strip())
  return dictionary

def can_make_word(possible_word, letter_pool):
  # Check if we have a letter for each character in possible word
  for character in possible_word:
    if character in letter_pool:
      # If we match, remove the letter from our letter pool
      letter_pool.remove(character)
    else:
      # We found a character not in our letter pool - failed!
      return False
  return True

def find_all_matches(letters):
  dictionary = load_dictionary()
  words = []
  for word in dictionary:
    for letter in global_letters:
      letters_to_check = letters + [letter]
      if can_make_word(word, letters_to_check):
        words.append(word)
  return words

words = set(find_all_matches(letters_in_hand))
for word in sorted(words):
  print word

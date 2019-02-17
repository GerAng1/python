"""This program will generate a random sum"""

from random import randint
from time import sleep

def get_user_guess():
  guess = int(raw_input("Guess a number: "))
  return guess

def roll_dice(number_of_sides):
  first_roll = randint(1, number_of_sides)
  second_roll = randint(1, number_of_sides)

  max_val = number_of_sides * 2
  
  print "The max value you can get is %d" % max_val
  
  guess = get_user_guess()
  
  if guess > 12:
    print "That's not possible"
    
  else:
    print("Rolling...")
    sleep(2)
    print "The first roll is... %d!" % first_roll
    sleep(1)
    print "The second roll is %d" % second_roll
    sleep(1)
    total_roll = first_roll + second_roll
    print "That's a total of %d" % total_roll
    sleep(1)
    
    if guess == total_roll:
      print "You won!"
      
    else:
      print "You lost :("
      

roll_dice(6)
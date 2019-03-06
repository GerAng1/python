Asignar valor default para parametro dentro de funcion
"""
# this is not valid
def greet_customer(special_item="bananas", grocery_store):
    # TODO code here


# this is valid
def greet_customer(special_item, grocery_store="Engrossing Grocers"):
    # TODO code here


Al llamarlo, si no pongo un valor para grocery_store, utilizara el DEFAULT"""

# Puedes return mas de un valor!!!

def square_point(x_value, y_value):
  x_2 = x_value * x_value
  y_2 = y_value * y_value
  return x_2, y_2

x_squared, y_squared = square_point(1, 3)
print(x_squared)
print(y_squared)

# Concatenando 
def repeat_stuff(stuff, num_repeats = 10):
  return stuff * num_repeats


lyrics = repeat_stuff('Row ', 3) + 'Your Boat. '
song = repeat_stuff(lyrics)

print(song)

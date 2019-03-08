# Asignar valor default para parametro dentro de funcion {
"""
# ERROR
def greet_customer(special_item = "bananas", grocery_store):
    // TODO code here

# VALID
def greet_customer(special_item, grocery_store = 3):
    // TODO code here

Al llamarlo, si no pongo un valor para grocery_store, utilizara el DEFAULT
"""
# }

# Puedes return mas de un valor!!! {
def square_point(x_value, y_value):
  x_2 = x_value * x_value
  y_2 = y_value * y_value
  return x_2, y_2

x_squared, y_squared = square_point(1, 3)
print(x_squared)
print(y_squared)
# }

# Concatenando {
def repeat_stuff(stuff, num_repeats = 10):
  return stuff * num_repeats


lyrics = repeat_stuff('Row ', 3) + 'Your Boat. '
song = repeat_stuff(lyrics)

print(song)
# }

# Puedes usar un metodo dentro de un metodo y definirlo todo en el return...
# {
def get_force(mass, acceleration):
  return mass * acceleration

def get_work(mass, acceleration, distance):
  return get_force(mass, acceleration) * distance

train_work = get_work(train_mass, train_acceleration, train_distance)
print("The train does " + str(train_work) + " Joules over " + str(train_distance) + " meters.")
# }

"""Creando una copia de una lista por valor y por referencia
    Copy of a list by value or reference """

my_list = [[2, 4, 6, 8], [1, 3, 5, 7]]

copy1 = [x[:] for x in my_list] # Paso por VALOR

copy2 = list(my_list) # Paso por referencia

copy3 = copy2[:] # Paso por referencia


print my_list[0]
print copy1
print copy2
print copy3

my_list[1][0] = 5
print ""
print my_list
print copy1
print copy2
print copy3

copy2[1][0] = 10
print ""
print my_list
print copy1
print copy2
print copy3
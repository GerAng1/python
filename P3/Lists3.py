# COMANDOS PARA LISTAS PYTHON 3

first_names = ['Ainsley', 'Ben', 'Chani', 'Depak']
age = []
age.append(42)

# Sumando listas
all_ages = age + [32, 41, 29]

# Juntando en un zip listas (1 con 1, 2 con 2...)
name_and_age = zip(first_names, all_ages)
name_and_age_list = list(name_and_age)

ids = list(range(0, 4, 2))

print(name_and_age)
print(name_and_age_list)
print(ids)

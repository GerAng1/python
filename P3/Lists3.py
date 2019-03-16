# https://www.programiz.com/python-programming/methods/list
################################################################
# COMANDOS PARA LISTAS PYTHON 3
################################################################

first_names = ['Ainsley', 'Ben', 'Chani', 'Depak']
age = []
age.append(42)
name = first_names.pop() # name = 'Depak'
print(first_names) # ['Ainsley', 'Ben', 'Chani']

################################################################
# Sumando listas
################################################################
all_ages = age + [32, 41, 29]

################################################################
# Juntando en un zip listas (1 con 1, 2 con 2...)
################################################################
name_and_age = zip(first_names, all_ages)
name_and_age_list = list(name_and_age)

ids = list(range(0, 4, 2))

print(name_and_age)
print(name_and_age_list)
print(ids)

################################################################
# Slicing cortar una lista
################################################################
suitcase = ['shirt', 'shirt', 'pants', 'pants', 'pajamas', 'books']

start = suitcase[:3] # ['shirt', 'shirt', 'pants']
end = suitcase[-2:] # ['pajamas', 'books']

################################################################
# Contar elementos dentrode una lista
################################################################
votes = ['Jake', 'Jake', 'Laurie', 'Laurie', 'Laurie', 'Jake', 'Jake', 'Jake', 'Laurie', 'Cassie', 'Cassie', 'Jake', 'Jake', 'Cassie', 'Laurie', 'Cassie', 'Jake', 'Jake', 'Cassie', 'Laurie']

jake_votes = votes.count('Jake')
print(jake_votes) # 9

################################################################
# Ordenar arreglos
################################################################
names = ['Xander', 'Buffy', 'Angel', 'Willow', 'Giles']
names.sort()
print(names) # ['Angel', 'Buffy', 'Giles', 'Willow', 'Xander']

# If we try sort(names), we will get a NameError.
# sort does not return anything.
# So, if we try to assign names.sort() to a variable,
# our new variable would be None

# ERROR MAL
print(names.sort()) # None

################################################################
# Unwrapping guardando valores de lista en variables
################################################################
my_info = ['gerry', 24, 'student']
name, age, occupation = my_info
print(name) # 'gerry'

################################################################
# LIST COMPREHENSION
################################################################
words = ["@coolguy35", "#nofilter", "@kewldawg54", "reply", "timestamp", "@matchamom", "follow", "#updog"]
usernames = []

#for word in words:
# if word[0] == '@':
#   usernames.append(word)
# USE:
usernames = [word + ' #likeme' for word in words if word[0] == '@']
# usernames = [word for word in words] seria una copia de words

hairstyles = ["bouffant", "pixie", "dreadlocks", "crew", "bowl", "bob", "mohawk", "flattop"]

prices = [30, 25, 40, 20, 20, 35, 50, 35]

cuts_under_30 = [hairstyles[i] for i in range(len(hairstyles)) if prices[i] < 30]
print(cuts_under_30) # ['pixie', 'crew', 'bowl']

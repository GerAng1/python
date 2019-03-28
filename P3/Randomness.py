# Import random below:
import random

# Create random_list below:
random_list = [random.randint(1,100) for num in range(101) ]

# Create randomer_number below:
randomer_number = random.choice(random_list)


# Print randomer_number below:
print(random_list)
print()
random_list.sort()
print(random_list)
print(randomer_number)

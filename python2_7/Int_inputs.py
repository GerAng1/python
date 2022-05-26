
# Modulo will always be numbes from 0 to n - 1
print 16 % 3
for i in range(4, 100, 3): # for format
    print "{}: % = {}".format(i, i % 3)

number = input("Give me any number: ")
number = int(number)
number = float(number)
print number


""" Typing '2/5' won't give 0.2
if using python 2.x.x
because 2 is int and 5 is int so answer is int (0.0)"""

a0 = 0.5
a1 = 1 - 2

func = a0.__str__() + " + " + a1.__str__() + " * x"
print func

age = float(input("Whats your age: "))
print age


# Create and fill list with 0's

tam = 5
array = [0.0 for col in range(tam)]


""" HOW TO DEFINE AND EVALUATE FUNCTIONS
function = func_keeper()
x = float(raw_input("What will be your 'x'?: "))
fx = func_evaluator(func, x)
print "Your 'x' is %f and your f(x) is %f." % (x, fx)"""

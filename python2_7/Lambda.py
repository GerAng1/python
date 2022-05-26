"""def func_keeper():
    print "Give me a function in python form."
    print "e.g. (x ** 2 + 1) / (1 - x) ** 2"
    func = raw_input("Give me a function in terms of x: ")
    return func"""


def func_evaluator(func, to_plot):
    f = lambda x: eval(func)
    fx = f(to_plot)
    return fx


function = func_keeper()
x = float(raw_input("What will be your 'x'?: "))
fx = func_evaluator(function, x)
print "Your 'x' is %f and your f(x) is %f." % (x, fx)

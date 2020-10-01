import math

from FuzzyMath.class_interval import Interval
from FuzzyMath.class_fuzzy_number import FuzzyNumber

# define two fuzzy numbers
a = FuzzyNumber(alphas=[0, 0.5, 1],
                alpha_cuts=[Interval.infimum_supremum(1, 3),
                            Interval.infimum_supremum(1.5, 2.5),
                            Interval.infimum_supremum(2, 2)])

b = FuzzyNumber(alphas=[0, 0.3, 0.6, 1],
                alpha_cuts=[Interval.infimum_supremum(0, 4),
                            Interval.infimum_supremum(1, 3),
                            Interval.infimum_supremum(1, 3),
                            Interval.infimum_supremum(2, 2)])

# one fuzzy number functions
print("--- representation a ---")
print(a)
print(repr(a))

print("\n")
print("--- in operator ---")
print("-1 in a: {}".format(-1 in a))
print("0 in a: {}".format(0 in a))
print("1 in a: {}".format(1 in a))
print("5 in a: {}".format(5 in a))
print("7 in a: {}".format(7 in a))

print("\n")
print("--- < > operators ---")
print("-1 < a: {}".format(-1 < a))
print("0 < a: {}".format(0 < a))
print("1 < a: {}".format(1 < a))
print("5 < a: {}".format(5 < a))
print("7 < a: {}".format(7 < a))

print("-1 > a: {}".format(-1 > a))
print("0 > a: {}".format(0 > a))
print("1 > a: {}".format(1 > a))
print("5 > a: {}".format(5 > a))
print("7 > a: {}".format(7 > a))

print("\n")
print("--- len function ---")
print(len(a))

print("\n")
print("--- == operator ---")
print("a == b: {}".format(a == b))
print("a == a: {}".format(a == a))

print("\n")
print("--- math operators a and number ---")
print("a + 1 : {}".format(repr(a + 1)))
print("1 + a : {}".format(repr(1 + a)))
print("a - 1 : {}".format(repr(a - 1)))
print("1 - a : {}".format(repr(1 - a)))
print("a * 2 : {}".format(repr(a * 2)))
print("2 * a : {}".format(repr(2 * a)))
print("a / 2 : {}".format(repr(a / 2)))
print("2 / a : {}".format(repr(2 / a)))

print("pow(a, 2) : {}".format(repr(pow(a, 2))))
print("a ** 2 : {}".format(repr(a ** 2)))

print("\n")
print("--- math operators a and b ---")
print("a + b : {}".format(repr(a + b)))
print("b + a : {}".format(repr(b + a)))
print("a - b : {}".format(repr(a - b)))
print("b - a : {}".format(repr(b - a)))
print("a * b : {}".format(repr(a * b)))
print("b * a : {}".format(repr(b * a)))
print("b / a : {}".format(repr(b / a)))

print("\n")
print("--- math ---")
print("a + 5 * b : {}".format(repr(a + 5 * b)))

print("\n")
print("--- math functions ---")
print("a.apply_function(math.sin) : {}".format(repr(a.apply_function(math.sin))))

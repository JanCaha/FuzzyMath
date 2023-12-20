import math

from FuzzyMath.class_factories import IntervalFactory
from FuzzyMath.class_fuzzy_number import FuzzyNumber
from FuzzyMath.class_interval import Interval

# define two fuzzy numbers
a = FuzzyNumber(
    alphas=[0, 0.5, 1],
    alpha_cuts=[
        IntervalFactory.infimum_supremum(1, 3),
        IntervalFactory.infimum_supremum(1.5, 2.5),
        IntervalFactory.infimum_supremum(2, 2),
    ],
)

b = FuzzyNumber(
    alphas=[0, 0.3, 0.6, 1],
    alpha_cuts=[
        IntervalFactory.infimum_supremum(0, 4),
        IntervalFactory.infimum_supremum(1, 3),
        IntervalFactory.infimum_supremum(1, 3),
        IntervalFactory.infimum_supremum(2, 2),
    ],
)

# one fuzzy number functions
print("--- representation a ---")
print(a)
print(repr(a))

print("\n")
print("--- in operator ---")
print(f"-1 in a: {-1 in a}")
print(f"0 in a: {0 in a}")
print(f"1 in a: {1 in a}")
print(f"5 in a: {5 in a}")
print(f"7 in a: {7 in a}")

print("\n")
print("--- < > operators ---")
print(f"-1 < a: {-1 < a}")
print(f"0 < a: {0 < a}")
print(f"1 < a: {1 < a}")
print(f"5 < a: {5 < a}")
print(f"7 < a: {7 < a}")

print(f"-1 > a: {-1 > a}")
print(f"0 > a: {0 > a}")
print(f"1 > a: {1 > a}")
print(f"5 > a: {5 > a}")
print(f"7 > a: {7 > a}")

print("\n")
print("--- len function ---")
print(len(a))

print("\n")
print("--- == operator ---")
print(f"a == b: {a == b}")
print(f"a == a: {a == a}")

print("\n")
print("--- math operators a and number ---")
print(f"a + 1 : {a + 1}")
print(f"1 + a : {1 + a}")
print(f"a - 1 : {a - 1}")
print(f"1 - a : {1 - a}")
print(f"a * 2 : {a * 2}")
print(f"2 * a : {2 * a}")
print(f"a / 2 : {a / 2}")
print(f"2 / a : {2 / a}")

print("pow(a, 2) : {}".format(repr(pow(a, 2))))
print("a ** 2 : {}".format(repr(a**2)))

print("\n")
print("--- math operators a and b ---")
print(f"a + b : {a + b}")
print(f"b + a : {b + a}")
print(f"a - b : {a - b}")
print(f"b - a : {b - a}")
print(f"a * b : {a * b}")
print(f"b * a : {b * a}")
print(f"b / a : {b / a}")

print("\n")
print("--- math ---")
print("a + 5 * b : {}".format(repr(a + 5 * b)))

print("\n")
print("--- math functions ---")
print(f"a.apply_function(math.sin) : {a.apply_function(math.sin)}")

from FuzzyMath.class_interval import Interval
from FuzzyMath.class_fuzzy_number import FuzzyNumber

a = FuzzyNumber(alphas=[0, 0.5, 1],
                alpha_cuts=[Interval.infimum_supremum(1, 3),
                            Interval.infimum_supremum(1.5, 2.5),
                            Interval.infimum_supremum(2, 2)])

b = FuzzyNumber(alphas=[0, 0.3, 0.6, 1],
                alpha_cuts=[Interval.infimum_supremum(0, 4),
                            Interval.infimum_supremum(1, 3),
                            Interval.infimum_supremum(1, 3),
                            Interval.infimum_supremum(2, 2)])

print(a.get_alpha_cut(1))

print(-1 in a)
print(0 in a)
print(1 in a)
print(5 in a)
print(7 in a)

print(a)

print(a + 1)
print(1 + a)
print(a + a)

print(a * 1)
print(2 * a)
print(a * a)

print(10 / a)
print(a / 10)

print(a ** 2)


# FuzzyNumber._iterate_alphas(a, b, Interval.__add__)
# FuzzyNumber._iterate_alphas(a, 1, Interval.__add__)
# FuzzyNumber._iterate_alphas(2, b, Interval.__radd__)


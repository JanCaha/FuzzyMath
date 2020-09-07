import unittest
import math

from FuzzyMath.class_fuzzy_number import FuzzyNumber
from FuzzyMath.class_interval import Interval


class FuzzyNumberTests(unittest.TestCase):

    def setUp(self) -> None:
        self.a = FuzzyNumber.triangular(1, 2, 3)
        self.b = FuzzyNumber.triangular(2, 3, 4)
        self.c = FuzzyNumber.triangular(-1, 0, 1)
        self.d = FuzzyNumber.trapezoidal(1, 2, 3, 4)
        self.e = FuzzyNumber.triangular(1, 2, 3, number_of_cuts=6)

    def test_fuzzynumber_creation(self):

        with self.assertRaisesRegex(TypeError, "must be a list"):
            FuzzyNumber(1, [])

        with self.assertRaisesRegex(TypeError, "must be a list"):
            FuzzyNumber([], 1)

        with self.assertRaisesRegex(ValueError, "Lists `alphas` and `alpha_cuts` must be of same length."):
            FuzzyNumber([1, 2, 3], [1, 2])

        with self.assertRaisesRegex(ValueError, "All elements of `alphas` must be from range"):
            FuzzyNumber([0, 0.5, 1, 1.1], [None]*4)

        with self.assertRaisesRegex(ValueError, "All elements of `alphas` must be int or float"):
            FuzzyNumber([0, 0.5, 1, "1.1"], [None]*4)

        with self.assertRaisesRegex(ValueError, "Values in `alphas` are not unique"):
            FuzzyNumber([0, 0.5, 1, 0.5], [None]*4)

        with self.assertRaisesRegex(ValueError, "`alphas` must contain both 0 and 1 alpha value"):
            FuzzyNumber([0, 0.5, 0.9], [None]*3)

        with self.assertRaisesRegex(ValueError, "`alphas` must contain both 0 and 1 alpha value"):
            FuzzyNumber([0.1, 0.5, 1], [None]*3)

        with self.assertRaisesRegex(TypeError, "All elements of `alpha_cuts` must be Interval"):
            FuzzyNumber([0, 1],
                        [Interval.two_values(0, 1),
                         5])

        with self.assertRaisesRegex(ValueError, "Interval on lower alpha level has to contain the higher level alpha cuts"):
            FuzzyNumber([0, 1],
                        [Interval.two_values(0, 1),
                         Interval.two_values(2, 2)])

        string_fn = '(0.0;1.0,3.0)(0.111111111111111;1.1,2.9)(0.222222222222222;1.2,2.8)(0.333333333333333;1.3,2.7)' \
                    '(0.444444444444444;1.4,2.6)(0.555555555555556;1.5,2.5)(0.666666666666667;1.6,2.4)' \
                    '(0.777777777777778;1.7,2.3)(0.888888888888889;1.8,2.2)(1.0;2.0,2.0)'

        self.assertIsInstance(FuzzyNumber.parse_string(string_fn), FuzzyNumber)

        string_fn = '(0.0;1,3)(0.5;1.9999,2.0001)(1.0;2,2)'

        self.assertIsInstance(FuzzyNumber.parse_string(string_fn), FuzzyNumber)

        with self.assertRaisesRegex(ValueError, "Cannot parse FuzzyNumber from this definition"):
            string_fn = '(0.0;1.0,3.0)(0.5;1.9999)(1.0;2.0,2.0)'
            FuzzyNumber.parse_string(string_fn)

        with self.assertRaisesRegex(ValueError, "element of Fuzzy Number"):
            string_fn = '(0.0;1.0,3.0)(0.5;2.0001,1.9999)(1.0;2.0,2.0)'
            FuzzyNumber.parse_string(string_fn)

        with self.assertRaisesRegex(ValueError, "element of Fuzzy Number"):
            string_fn = '(0.0;1.0,3.0)(1.1;1.9999,2.0001)(1.0;2.0,2.0)'
            FuzzyNumber.parse_string(string_fn)

        with self.assertRaisesRegex(ValueError, "Interval on lower alpha level has to contain the higher"):
            string_fn = '(0.0;1.0,3.0)(0.5;2.5,2.75)(1.0;2.0,2.0)'
            FuzzyNumber.parse_string(string_fn)

    def test_alphas(self):
        self.assertListEqual(self.a.alpha_levels, [0, 1])
        self.assertListEqual(self.e.alpha_levels, [0, 0.2, 0.4, 0.6, 0.8, 1])

    def test_alpha_cuts(self):
        intervals = [Interval.infimum_supremum(1, 3),
                     Interval.infimum_supremum(2, 2)]
        self.assertListEqual(intervals, list(self.a.alpha_cuts))

    def test_alpha_cut(self):
        self.assertEqual(Interval.two_values(1, 3), self.a.get_alpha_cut(0))
        self.assertEqual(Interval.two_values(1.25, 2.75), self.a.get_alpha_cut(0.25))
        self.assertEqual(Interval.two_values(1.5, 2.5), self.a.get_alpha_cut(0.5))
        self.assertEqual(Interval.two_values(1.75, 2.25), self.a.get_alpha_cut(0.75))
        self.assertEqual(Interval.two_values(2, 2), self.a.get_alpha_cut(1))

    def test_contain(self):
        self.assertTrue(2 in self.a)
        self.assertTrue(1 in self.a)
        self.assertTrue(1.1 in self.a)
        self.assertTrue(2.9 in self.a)
        self.assertTrue(3 in self.a)
        self.assertFalse(0.999 in self.a)
        self.assertFalse(3.001 in self.a)

    def test_get_alpha_cut_values(self):
        self.assertListEqual(FuzzyNumber.get_alpha_cut_values(6, precision=4), [0, 0.2, 0.4, 0.6, 0.8, 1])
        self.assertListEqual(FuzzyNumber.get_alpha_cut_values(2, precision=4), [0, 1])
        self.assertListEqual(FuzzyNumber.get_alpha_cut_values(11, precision=8),
                             [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])

        with self.assertRaisesRegex(ValueError, "`number_of_cuts` has to be integer and higher than 1"):
            FuzzyNumber.get_alpha_cut_values("str", precision=2)

        with self.assertRaisesRegex(ValueError, "`number_of_cuts` has to be integer and higher than 1"):
            FuzzyNumber.get_alpha_cut_values(5.0, precision=2)

        with self.assertRaisesRegex(ValueError, "`number_of_cuts` has to be integer and higher than 1"):
            FuzzyNumber.get_alpha_cut_values(1, precision=2)

    def test_add(self):
        self.assertEqual(FuzzyNumber.triangular(2, 3, 4),
                         self.a + 1)
        self.assertEqual(FuzzyNumber.triangular(2, 3, 4),
                         1 + self.a)
        self.assertEqual(FuzzyNumber.triangular(3, 5, 7),
                         self.a + self.b)
        self.assertEqual(FuzzyNumber.triangular(3, 5, 7),
                         self.b + self.a)
        self.assertEqual(FuzzyNumber.triangular(0, 2, 4),
                         self.a + self.c)

    def test_sub(self):
        self.assertEqual(FuzzyNumber.triangular(0, 1, 2),
                         self.a - 1)
        self.assertEqual(FuzzyNumber.triangular(-2, -1, 0),
                         1 - self.a)
        self.assertEqual(FuzzyNumber.triangular(-3, -1, 1),
                         self.a - self.b)
        self.assertEqual(FuzzyNumber.triangular(-1, 1, 3),
                         self.b - self.a)
        self.assertEqual(FuzzyNumber.triangular(0, 2, 4),
                         self.a - self.c)

    def test_truediv(self):
        self.assertEqual(FuzzyNumber.triangular(0.5, 1, 1.5),
                         self.a / 2)

        with self.assertRaisesRegex(ArithmeticError, "Cannot divide by 0"):
            self.assertEqual(FuzzyNumber.triangular(0.5, 1, 1.5),
                             self.a / 0)

        self.assertEqual(FuzzyNumber.triangular(self.a.min / self.b.max,
                                                self.a.kernel.min / self.b.kernel.min,
                                                self.a.max / self.b.min),
                         self.a / self.b)

        self.assertEqual(FuzzyNumber.triangular(5 / self.a.max, 5 / self.a.kernel.min, 5 / self.a.min),
                         5 / self.a)

    def test_pow(self):
        power = 2
        self.assertEqual(FuzzyNumber.triangular(1**power, 2**power, 3**power),
                         pow(self.a, power))

    def test_function(self):
        fn = FuzzyNumber.triangular(-math.pi/2, 0, math.pi/2, 11, 8)

        fn_cos = fn.apply_function(math.cos)

        self.assertAlmostEqual(-0, fn_cos.min, places=8)
        self.assertAlmostEqual(1.0, fn_cos.max, places=8)
        self.assertAlmostEqual(1.0, fn_cos.kernel.min, places=8)

        fn_sin = fn.apply_function(math.sin)

        self.assertAlmostEqual(-1.0, fn_sin.min, places=8)
        self.assertAlmostEqual(1.0, fn_sin.max, places=8)
        self.assertAlmostEqual(0, fn_sin.kernel.min, places=8)

    def test_comparisons(self):

        self.assertFalse(self.a == self.b)
        self.assertTrue(self.a == FuzzyNumber.triangular(1, 2, 3))

        self.assertTrue(self.c < self.b)
        self.assertFalse(self.c > self.b)

        self.assertTrue(self.c < 2)
        self.assertFalse(self.c < -2)
        self.assertTrue(self.c > -5)
        self.assertFalse(self.c > 5)

        with self.assertRaises(TypeError):
            var = self.a > "test"

    def test_complex_comparisons(self):
        fn_a = FuzzyNumber.triangular(2, 3, 5)
        fn_b = FuzzyNumber.triangular(1.5, 4, 4.8)

        with self.subTest("{} \n {}".format(fn_a, fn_b)):

            self.assertAlmostEqual(fn_a.possibility_exceedance(fn_b),
                                   0.7777777777777777)
            self.assertAlmostEqual(fn_a.necessity_exceedance(fn_b),
                                   0.4285714285714289)
            self.assertAlmostEqual(fn_a.possibility_strict_exceedance(fn_b),
                                   0.357142857142857)
            self.assertAlmostEqual(fn_a.necessity_strict_exceedance(fn_b),
                                   0.0)

            self.assertAlmostEqual(fn_a.possibility_undervaluation(fn_b),
                                   1.0)
            self.assertAlmostEqual(fn_a.necessity_undervaluation(fn_b),
                                   0.6428571428571429)
            self.assertAlmostEqual(fn_a.possibility_strict_undervaluation(fn_b),
                                   0.5714285714285711)
            self.assertAlmostEqual(fn_a.necessity_strict_undervaluation(fn_b),
                                   0.22222222222222235)

        fn_a = FuzzyNumber.triangular(1.7, 2.7, 2.8)
        fn_b = FuzzyNumber.triangular(0, 1.8, 2.2)

        with self.subTest("{} \n {}".format(fn_a, fn_b)):

            self.assertAlmostEqual(fn_a.possibility_exceedance(fn_b),
                                   1.0)
            self.assertAlmostEqual(fn_a.necessity_exceedance(fn_b),
                                   0.9642857142857143)
            self.assertAlmostEqual(fn_a.possibility_strict_exceedance(fn_b),
                                   1.0)
            self.assertAlmostEqual(fn_a.necessity_strict_exceedance(fn_b),
                                   0.642857142857143)

            self.assertAlmostEqual(fn_a.possibility_undervaluation(fn_b),
                                   0.35714285714285726)
            self.assertAlmostEqual(fn_a.necessity_undervaluation(fn_b),
                                   0.0)
            self.assertAlmostEqual(fn_a.possibility_strict_undervaluation(fn_b),
                                   0.03571428571428574)
            self.assertAlmostEqual(fn_a.necessity_strict_undervaluation(fn_b),
                                   0.0)

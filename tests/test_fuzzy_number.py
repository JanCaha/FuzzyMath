import unittest
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

        with self.assertRaisesRegex(ValueError, "All elements of `alphas` must be int or float from range"):
            FuzzyNumber([0, 0.5, 1, 1.1], [None]*4)

        with self.assertRaisesRegex(ValueError, "All elements of `alphas` must be int or float from range"):
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


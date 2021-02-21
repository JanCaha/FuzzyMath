import unittest
import math

from FuzzyMath.class_interval import Interval


class IntervalTests(unittest.TestCase):

    def setUp(self) -> None:
        self.a = Interval.infimum_supremum(1, 3)
        self.b = Interval.infimum_supremum(2, 5)
        self.c = Interval.infimum_supremum(4, 7)
        self.d = Interval.infimum_supremum(-2, 3)
        self.e = Interval.infimum_supremum(-1, 1)
        self.f = Interval.empty()

    def test_interval_creation(self):
        self.assertIsInstance(Interval.two_values(1, 3), Interval)
        self.assertIsInstance(Interval.two_values(3, 1), Interval)
        self.assertIsInstance(Interval.infimum_supremum(1, 3), Interval)
        self.assertIsInstance(Interval.midpoint_width(2, 1), Interval)

        with self.assertRaisesRegex(ArithmeticError,
                                    "`width` of interval must number higher or at least equal to 0."):
            Interval.midpoint_width(0, -1)

        with self.assertRaisesRegex(ValueError, "The interval is invalid. `minimum` "
                                                "must be lower or equal to `maximum`"):
            Interval.infimum_supremum(3, 1)

        with self.assertRaisesRegex(ValueError, "`precision` should be value from range `0` to `15`"):
            Interval(1, 3, precision=-1)
            Interval(1, 3, precision=16)

        with self.assertWarnsRegex(UserWarning, "Using default value of precision"):
            Interval(1, 3, precision="pre")

        interval = Interval.two_values(1.0000000000001, 3.000000009, precision=2)
        self.assertEqual(interval.min, 1)
        self.assertEqual(interval.max, 3)

        interval = Interval.parse_string("[1, 2.5]")
        self.assertEqual(interval, Interval(1, 2.5))

        with self.assertRaisesRegex(ValueError, "Cannot parse Interval from this definition"):
            Interval.parse_string("[1, 2.5, 5]")

        with self.assertRaisesRegex(ValueError, "Cannot parse Interval from this definition"):
            Interval.parse_string("[]")

        with self.assertRaisesRegex(ValueError, "Cannot parse Interval from this definition"):
            Interval.parse_string("[\"aa\", \"b\"]")

    def test_degenerate_interval(self):
        self.assertTrue(Interval.infimum_supremum(2, 2).degenerate)
        self.assertFalse(Interval.infimum_supremum(2, 3).degenerate)

    def test_mid_point(self):
        a = Interval.two_values(1, 2)
        self.assertEqual(1.5, a.mid_point)
        b = Interval.midpoint_width(2, 2)
        self.assertEqual(2, b.mid_point)

    def test_contains(self):
        interval = Interval.infimum_supremum(1, 5)
        self.assertTrue(2 in interval)
        self.assertTrue(1 in interval)
        self.assertTrue(3.59 in interval)
        self.assertFalse(0.999999 in interval)
        self.assertFalse(5.0001 in interval)

        self.assertFalse(Interval.two_values(6, 7) in interval)
        self.assertFalse(Interval.two_values(0, 3) in interval)
        self.assertTrue(Interval.two_values(2, 4) in interval)

        with self.assertRaisesRegex(TypeError, "Cannot test if object of type "):
           "str" in interval
           True in interval

    def test_intersects(self):
        self.assertTrue(self.a.intersects(self.b))
        self.assertTrue(self.b.intersects(self.a))
        self.assertTrue(self.b.intersects(self.c))
        self.assertTrue(self.c.intersects(self.b))

        self.assertFalse(self.a.intersects(self.c))
        self.assertFalse(self.c.intersects(self.a))

    def test_intersection(self):
        self.assertEqual(Interval.two_values(2, 3), self.a.intersection(self.b))
        self.assertEqual(Interval.two_values(4, 5), self.b.intersection(self.c))

        with self.assertRaisesRegex(ArithmeticError, "do not intersect"):
            self.a.intersection(self.c)

    def test_union(self):
        self.assertEqual(Interval.two_values(1, 5), self.a.union(self.b))
        self.assertEqual(Interval.two_values(2, 7), self.b.union(self.c))

        with self.assertRaisesRegex(ArithmeticError, "do not intersect"):
            self.a.union(self.c)

    def test_union_hull(self):
        self.assertEqual(Interval.two_values(1, 7), self.a.union_hull(self.c))

    def test_add(self):
        self.assertEqual(Interval.two_values(self.a.min + 1, self.a.max + 1),
                         self.a + 1)
        self.assertEqual(Interval.two_values(1 + self.a.min, 1 + self.a.max),
                         1 + self.a)
        self.assertEqual(Interval.two_values(self.a.min + self.b.min, self.a.max + self.b.max),
                         self.a + self.b)
        self.assertEqual(Interval.two_values(self.a.min + self.e.min, self.a.max + self.e.max),
                         self.a + self.e)

        with self.assertRaisesRegex(TypeError, "unsupported operand"):
            self.a + "str"
            "str" + self.a

    def test_sub(self):
        self.assertEqual(Interval.two_values(self.a.min - 1, self.a.max - 1),
                         self.a - 1)
        self.assertEqual(Interval.two_values(1 - self.a.min, 1 - self.a.max),
                         1 - self.a)
        self.assertEqual(Interval.two_values(self.a.min - self.b.max, self.a.max - self.b.min),
                         self.a - self.b)

        with self.assertRaisesRegex(TypeError, "unsupported operand"):
            self.a - "str"
            "str" - self.a

    def test_mul(self):
        self.assertEqual(Interval.two_values(self.a.min * 2, self.a.max * 2),
                         self.a * 2)
        self.assertEqual(Interval.two_values(self.a.min * 2, self.a.max * 2),
                         2 * self.a)
        self.assertEqual(Interval.two_values(self.a.min * self.b.min, self.a.max * self.b.max),
                         self.a * self.b)

        with self.assertRaisesRegex(TypeError, "multiply sequence"):
            self.a * "str"
            "str" * self.a

    def test_truediv(self):
        self.assertEqual(Interval.two_values(self.a.min / 2, self.a.max / 2),
                         self.a / 2)
        self.assertEqual(Interval.two_values(2 / self.a.min, 2 / self.a.max),
                         2 / self.a)
        self.assertEqual(Interval.two_values(self.a.min / self.b.max, self.a.max / self.b.min),
                         self.a / self.b)

        with self.assertRaisesRegex(TypeError, "unsupported operand"):
            self.a / "str"

        with self.assertRaisesRegex(ArithmeticError, "Cannot divide by 0"):
            self.a / 0

        with self.assertRaisesRegex(ArithmeticError, "Cannot divide by interval that contains `0`"):
            self.a / self.d

    def test_pow(self):
        self.assertEqual(Interval.two_values(1, 9), self.a ** 2)
        self.assertEqual(Interval.two_values(1, 27), self.a ** 3)

        self.assertEqual(Interval.two_values(0, 9), self.d ** 2)
        self.assertEqual(Interval.two_values(-8, 27), self.d ** 3)

    def test_neg(self):
        self.assertEqual(Interval.two_values(self.a.min * (-1), self.a.max * (-1)),
                         -self.a)
        self.assertEqual(Interval.two_values(self.d.min * (-1), self.d.max * (-1)),
                         -self.d)

    def test_eq(self):
        self.assertTrue(self.a == self.a)
        self.assertFalse(self.b == self.a)

    def test_lt(self):
        self.assertTrue(self.a < self.c)
        self.assertTrue(self.d < self.c)
        self.assertFalse(self.a < self.b)

    def test_gt(self):
        self.assertTrue(self.c > self.a)
        self.assertTrue(self.c > self.d)
        self.assertFalse(self.b > self.a)

    def test_lt_gt(self):
        self.assertEqual(self.a < self.c, self.c > self.a)
        self.assertEqual(self.d < self.c, self.c > self.d)

    def test_apply_function(self):

        # position argument not supported by the function
        with self.assertRaisesRegex(TypeError, "too many positional arguments"):
            self.a.apply_function(math.log2, 5)

        # keyword argument that does not exist
        with self.assertRaisesRegex(TypeError, "got an unexpected keyword argument 'c'"):
            self.a.apply_function(math.log2, c=5)

        self.assertAlmostEqual(math.log2(self.a.min), self.a.apply_function(math.log2).min)
        self.assertAlmostEqual(math.log2(self.a.max), self.a.apply_function(math.log2).max)

        self.assertAlmostEqual(-1, self.b.apply_function(math.cos).min, places=5)
        self.assertAlmostEqual(0.28366, self.b.apply_function(math.cos).max, places=5)

        self.assertEqual(Interval.two_values(1, 9),
                         self.a.apply_function(math.pow, 2, number_elements=10))

    def test_is_empty(self):
        self.assertTrue(self.f.is_empty)
        self.assertFalse(self.a.is_empty)

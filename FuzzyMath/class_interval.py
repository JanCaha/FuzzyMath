from __future__ import annotations
from typing import List
from types import FunctionType, BuiltinFunctionType
from inspect import signature, BoundArguments

import numpy as np

from FuzzyMath.fuzzymath_utils import set_up_precision


class Interval:

    __DEFAULT_PRECISION = 15

    __slots__ = ("_min", "_max", "_precision", "_degenerate")

    def __init__(self, a: float, b: float, precision: int = None):

        precision = set_up_precision(precision, self.__DEFAULT_PRECISION)

        a = float(a)
        b = float(b)

        self._degenerate = False

        minimum = min(a, b)
        maximum = max(a, b)

        self._precision = int(precision)
        self._min = round(minimum, self._precision)
        self._max = round(maximum, self._precision)

        if self._min == self._max:
            self._degenerate = True

    @classmethod
    def infimum_supremum(cls, minimum: float, maximum: float, precision: int = None) -> Interval:

        if minimum > maximum:
            raise ValueError("The interval is invalid. `minimum` must be lower or equal to"
                             " `maximum`. Currently it is `{0}` <= `{1}`, which does not hold."
                             .format(minimum, maximum))

        return cls(minimum, maximum, precision=precision)

    @classmethod
    def two_values(cls, a: float, b: float, precision: int = None) -> Interval:
        return cls(a, b, precision=precision)

    @classmethod
    def midpoint_width(cls, midpoint: float, width: float, precision: int = None) -> Interval:

        if width < 0:
            raise ArithmeticError("`width` of interval must number higher or at least equal to 0. "
                                  "The value `{0}` does not fulfill this.".format(width))

        midpoint = float(midpoint)
        width = float(width)

        a = midpoint - (width/2)
        b = midpoint + (width/2)

        return cls(a, b, precision=precision)

    def __repr__(self):
        return "[{0}, {1}]".format(self.min, self.max)

    @property
    def min(self) -> float:
        return self._min

    @property
    def max(self) -> float:
        return self._max

    @property
    def precision(self) -> int:
        return self._precision

    @property
    def degenerate(self) -> bool:
        return self._degenerate

    @property
    def width(self) -> float:
        return self._max - self._min

    @property
    def mid_point(self) -> float:
        if self.degenerate:
            return self._min
        else:
            return (self._min + self.max)/2

    def __contains__(self, item) -> bool:
        if isinstance(item, (int, float)):
            return self.min <= item <= self.max
        elif isinstance(item, Interval):
            return self.min <= item.min and item.max <= self.max
        else:
            raise TypeError("Cannot test if object of type `{0}` is in Interval. Only implemented for `float`, "
                            "`int` and `Interval`.".format(type(item).__name__))

    def intersects(self, other) -> bool:

        if other.max < self.min:
            return False

        if self.max < other.min:
            return False

        return True

    def intersection(self, other) -> Interval:

        if self.intersects(other):
            return Interval(max(self.min, other.min), min(self.max, other.max))
        else:
            raise ArithmeticError("Intervals `{0}` and `{1}` do not intersect, "
                                  "cannot construct intersection.".format(self, other))

    def union(self, other) -> Interval:

        if self.intersects(other):
            return Interval(min(self.min, other.min), max(self.max, other.max))
        else:
            raise ArithmeticError("Intervals `{0}` and `{1}` do not intersect, "
                                  "cannot construct valid union.".format(self, other))

    def union_hull(self, other) -> Interval:
        return Interval(min(self.min, other.min), max(self.max, other.max))

    def is_negative(self) -> bool:
        return self.max < 0

    def is_not_positive(self) -> bool:
        return self.max <= 0

    def is_positive(self) -> bool:
        return 0 < self.min

    def is_not_negative(self) -> bool:
        return 0 <= self.min

    def is_more_positive(self) -> bool:
        return 0 <= self.mid_point

    def apply_function(self,
                       function: (FunctionType, BuiltinFunctionType),
                       *args,
                       monotone: bool = False,
                       number_elements: float = 1000,
                       **kwargs) -> Interval:

        if not isinstance(function, (FunctionType, BuiltinFunctionType)):
            raise TypeError("`function` needs to be a function. It is `{0}`."
                            .format(type(function).__name__))

        if self.degenerate:
            elements = [self.min]
        elif monotone:
            elements = [self.min, self.max]
        else:
            step = (self.max-self.min)/number_elements
            elements = np.arange(self.min,
                                 self.max + 0.1*step,
                                 step=step).tolist()

            elements = [round(x, self.precision) for x in elements]

        function_signature = signature(function)

        results = [0]*len(elements)

        for i in range(0, len(elements)):
            bound_params: BoundArguments = function_signature.bind(elements[i], *args, **kwargs)
            bound_params.apply_defaults()

            results[i] = function(*bound_params.args, **bound_params.kwargs)

        return Interval.infimum_supremum(min(results), max(results), precision=self.precision)

    def __add__(self, other) -> Interval:
        if isinstance(other, (float, int)):
            return Interval(self.min + other, self.max + other, precision=self.precision)
        elif isinstance(other, Interval):
            return Interval(self.min + other.min, self.max + other.max, precision=self.precision)
        else:
            return NotImplemented

    def __radd__(self, other) -> Interval:
        return self + other

    def __sub__(self, other) -> Interval:
        if isinstance(other, (float, int)):
            return Interval(self.min - other, self.max - other, precision=self.precision)
        elif isinstance(other, Interval):
            return Interval(self.min - other.max, self.max - other.min, precision=self.precision)
        else:
            return NotImplemented

    def __rsub__(self, other) -> Interval:
        if isinstance(other, (float, int)):
            return Interval(other - self.min, other - self.max, precision=self.precision)
        else:
            return NotImplemented

    def __mul__(self, other) -> Interval:
        if isinstance(other, (float, int)):
            values = [self.min * other,
                      self.min * other,
                      self.max * other,
                      self.max * other]
            return Interval(min(values), max(values), precision=self.precision)
        elif isinstance(other, Interval):
            values = [self.min * other.min,
                      self.min * other.max,
                      self.max * other.min,
                      self.max * other.max]
            return Interval(min(values), max(values), precision=self.precision)
        else:
            return NotImplemented

    def __rmul__(self, other) -> Interval:
        return self * other

    def __truediv__(self, other) -> Interval:
        if isinstance(other, (float, int)):

            if other == 0:
                raise ArithmeticError("Cannot divide by 0.")

            values = [self.min / other,
                      self.min / other,
                      self.max / other,
                      self.max / other]
            return Interval(min(values), max(values), precision=self.precision)
        elif isinstance(other, Interval):

            if 0 in other:
                raise ArithmeticError("Cannot divide by interval that contains `0`. "
                                      "The interval is `{0}`.".format(other))

            values = [self.min / other.min,
                      self.min / other.max,
                      self.max / other.min,
                      self.max / other.max]
            return Interval(min(values), max(values), precision=self.precision)

        else:
            return NotImplemented

    def __rtruediv__(self, other) -> Interval:
        if isinstance(other, (float, int)):
            values = [other / self.min,
                      other / self.min,
                      other / self.max,
                      other / self.max]
            return Interval(min(values), max(values), precision=self.precision)
        else:
            return NotImplemented

    def __pow__(self, power) -> Interval:
        if isinstance(power, int):
            min_power = self.min ** power
            max_power = self.max ** power

            if (power%2) == 0:
                if self.min <= 0 <= self.max:
                    min_res = min(0, max(min_power, max_power))
                    max_res = max(0, max(min_power, max_power))
                else:
                    min_res = min(min_power, max_power)
                    max_res = max(min_power, max_power)
            else:
                min_res = min(min_power, max_power)
                max_res = max(min_power, max_power)

            return Interval(min_res, max_res, precision=self.precision)
        else:
            return NotImplemented

    # def __abs__(self):
    #     return Interval.two_values(math.fabs(self.min),
    #                                math.fabs(self.max), precision=self.precision)

    def __neg__(self) -> Interval:
        return Interval.two_values(self.min * (-1), self.max * (-1), precision=self.precision)

    def __eq__(self, other) -> bool:
        if isinstance(other, Interval):
            return self.min == other.min and \
                   self.max == other.max and \
                   self.precision == other.precision
        else:
            return NotImplemented

    def __lt__(self, other) -> bool:
        return self.max < other.min

    def __gt__(self, other) -> bool:
        return self.min > other.max

    def __hash__(self) -> int:
        return hash((self.min, self.max, self.precision))

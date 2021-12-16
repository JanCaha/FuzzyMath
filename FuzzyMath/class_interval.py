from __future__ import annotations
from typing import Callable
from types import FunctionType, BuiltinFunctionType
from inspect import signature, BoundArguments
import math
import re

import numpy as np

from .fuzzymath_utils import (get_precision,
                              set_up_precision)


class Interval:
    """
    Interval representation.

    ...

    Attributes
    ----------
    _min: float
        Minimal value of interval.

    _max: float
        Maximal value of interval.

    _precision: int
        Number of decimals used as precision for this interval.

    _degenerate: bool
        Is the interval degenerate? Degenerate interval have _min == _max.
    """

    __slots__ = ("_min", "_max", "_precision", "_degenerate")

    def __init__(self, a: float, b: float, precision: int = None):
        """
        Default constructor of interval. But generally it is more useful to use functions `Interval.infimum_supremum()`,
         `Interval.empty()`, `Interval.two_values()` and `Interval.midpoint_width()` instead of this function.

        Parameters
        ----------
        a: float
        b: float
        precision: int
            Precision of the interval, default value is `None`. If `None` then package wide default value is used.
        """
        a = float(a)
        b = float(b)

        if not precision:
            precision = get_precision()
        else:
            precision = set_up_precision(precision)

        self._degenerate = False

        minimum = min(a, b)
        maximum = max(a, b)

        self._precision = int(precision)
        self._min = round(minimum, self._precision)
        self._max = round(maximum, self._precision)

        if self._min == self._max:
            self._degenerate = True

    @classmethod
    def empty(cls) -> Interval:
        """
        Creates empty interval, which has no values.

        Returns
        -------
        Interval
        """
        return cls(float("nan"), float("nan"))

    @classmethod
    def infimum_supremum(cls, minimum: float, maximum: float, precision: int = None) -> Interval:
        """
        Interval defined by minimum and maximum.

        Parameters
        ----------
        minimum: float

        maximum: float

        precision: int
            Precision of the interval, default value is `None`. If `None` then package wide default value is used.

        Returns
        -------
        Interval

        Raises
        -------
        ValueError
            If `minimum > maximum` which is not valid interval for this definition.
        """

        if minimum > maximum:
            raise ValueError("The interval is invalid. `minimum` must be lower or equal to"
                             " `maximum`. Currently it is `{0}` <= `{1}`, which does not hold."
                             .format(minimum, maximum))

        return cls(minimum, maximum, precision=precision)

    @classmethod
    def two_values(cls, a: float, b: float, precision: int = None) -> Interval:
        """
        Interval defined by two values.

        Parameters
        ----------
        a: float

        b: float

        precision: int
            Precision of the interval, default value is `None`. If `None` then package wide default value is used.

        Returns
        -------
        Interval
        """
        return cls(a, b, precision=precision)

    @classmethod
    def midpoint_width(cls, midpoint: float, width: float, precision: int = None) -> Interval:
        """
        Interval defined by midpoint and width. The interval is [midpoint - width, midpoint + width].

        Parameters
        ----------
        midpoint: float

        width: float

        precision: int
            Precision of the interval, default value is `None`. If `None` then package wide default value is used.

        Returns
        -------
        Interval

        Raises
        -------
        ArithmeticError
            If `width < 0` which is not valid width definition.
        """
        if width < 0:
            raise ArithmeticError("`width` of interval must number higher or at least equal to 0. "
                                  "The value `{0}` does not fulfill this.".format(width))

        midpoint = float(midpoint)
        width = float(width)

        a = midpoint - (width / 2)
        b = midpoint + (width / 2)

        return cls(a, b, precision=precision)

    @classmethod
    def parse_string(cls,
                     string: str,
                     precision: int = None) -> Interval:
        """
        Creates `Interval` based on input string. The input string should be output of `__repr__()` function of
        `Interval`.

        Parameters
        ----------
        string: str

        precision: int

        Returns
        -------
        Interval
        """

        if not precision:
            precision = get_precision()
        else:
            precision = set_up_precision(precision)

        re_values = re.compile(r"\d+\.?\d*")

        numbers = re_values.findall(string)

        if len(numbers) != 2:
            raise ValueError("Cannot parse Interval from this definition. "
                             "Element does not provide 2 values (minimal and maximal).")

        return cls.two_values(numbers[0], numbers[1], precision=precision)

    def __repr__(self):
        """
        Representation of Interval.

        Returns
        -------
        str
        """
        return "[{0}, {1}]".format(self.min, self.max)

    @property
    def min(self) -> float:
        """
        Minimal value of `Interval`.

        Returns
        -------
        float
        """
        return self._min

    @property
    def max(self) -> float:
        """
        Maximal value of `Interval`.

        Returns
        -------
        float
        """
        return self._max

    @property
    def precision(self) -> int:
        """
        Returns precision used in this `Interval`.

        Returns
        -------
        int
        """
        return int(self._precision)

    @property
    def degenerate(self) -> bool:
        """
        Is this `Interval` degenerate? Degenerate Interval have minimum == maximum.

        Returns
        -------
        bool
        """
        return self._degenerate

    @property
    def width(self) -> float:
        """
        Width of interval. Width is equal to maximum - minimum.

        Returns
        -------
        float
        """
        return self._max - self._min

    @property
    def mid_point(self) -> float:
        """
        Middle point of `Interval`. Middle point is calculated as (minimum + maximum) / 2.

        Returns
        -------
        float
        """
        if self.degenerate:
            return self._min
        else:
            return (self._min + self.max) / 2

    @property
    def is_empty(self) -> bool:
        """
        Checks if the `Interval` is empty.

        Returns
        -------
        bool
        """
        return math.isnan(self.min) and math.isnan(self.max)

    def __contains__(self, item) -> bool:
        if isinstance(item, (int, float)):
            return self.min <= item <= self.max
        elif isinstance(item, Interval):
            return self.min <= item.min and item.max <= self.max
        else:
            raise TypeError("Cannot test if object of type `{0}` is in Interval. Only implemented for `float`, "
                            "`int` and `Interval`.".format(type(item).__name__))

    def intersects(self, other: Interval) -> bool:
        """
        Does this `Interval` intersects to `other`.

        Parameters
        ----------
        other: Interval

        Returns
        -------
        bool
        """
        if other.max < self.min:
            return False

        if self.max < other.min:
            return False

        return True

    def intersection(self, other: Interval) -> Interval:
        """
        Returns intersection of two `Interval`s.

        Parameters
        ----------
        other: Interval

        Returns
        -------
        Interval

        Raises
        -------
        ArithmeticError
            If this and other `Interval`s do not intersect.
        """
        if self.intersects(other):
            return Interval(max(self.min, other.min), min(self.max, other.max))
        else:
            raise ArithmeticError("Intervals `{0}` and `{1}` do not intersect, "
                                  "cannot construct intersection.".format(self, other))

    def union(self, other) -> Interval:
        """
        Returns union of two `Interval`s.

        Parameters
        ----------
        other: Interval

        Returns
        -------
        Interval

        Raises
        -------
        ArithmeticError
            If this and other `Interval`s do not intersect.
        """
        if self.intersects(other):
            return Interval(min(self.min, other.min), max(self.max, other.max))
        else:
            raise ArithmeticError("Intervals `{0}` and `{1}` do not intersect, "
                                  "cannot construct valid union.".format(self, other))

    def union_hull(self, other) -> Interval:
        """
        Returns union hull of two `Interval`s. Union hull is the widest interval covering both intervals.

        Parameters
        ----------
        other: Interval

        Returns
        -------
        Interval
        """
        return Interval(min(self.min, other.min), max(self.max, other.max))

    def is_negative(self) -> bool:
        """
        Checks if the `Interval` is strictly negative. Maximum < 0.

        Returns
        -------
        bool
        """
        return self.max < 0

    def is_not_positive(self) -> bool:
        """
        Checks if the `Interval` is not positive. Maximum <= 0.

        Returns
        -------
        bool
        """
        return self.max <= 0

    def is_positive(self) -> bool:
        """
        Checks if the `Interval` is strictly positive. Minimum > 0.

        Returns
        -------
        bool
        """
        return 0 < self.min

    def is_not_negative(self) -> bool:
        """
        Checks if the `Interval` is not negative. Minimum >= 0.

        Returns
        -------
        bool
        """
        return 0 <= self.min

    def is_more_positive(self) -> bool:
        """
        Checks if the midpoint of the interval is positive.

        Returns
        -------
        bool
        """
        return 0 <= self.mid_point

    def apply_function(self,
                       function: Callable,
                       *args,
                       monotone: bool = False,
                       number_elements: float = 1000,
                       **kwargs) -> Interval:
        """
        Apply mathematical function to interval.

        Parameters
        ----------
        function: (FunctionType, BuiltinFunctionType)
            Function to apply to fuzzy number.

        args
            Postional arguments for the `function`.

        monotone: bool
            Is the function monotone? Default `False`. If `True` can significantly speed up calculation.

        number_elements: int
            Number of elements to divide fuzzy number into, if the function is not monotone. Default is `1000`.

        kwargs
            Named arguments to pass into `function`.

        Returns
        -------
        Interval
            New `Interval`.
        """

        if not isinstance(function, (FunctionType, BuiltinFunctionType)):
            raise TypeError("`function` needs to be a function. It is `{0}`."
                            .format(type(function).__name__))

        if self.degenerate:
            elements = [self.min]
        elif monotone:
            elements = [self.min, self.max]
        else:
            step = (self.max - self.min) / number_elements
            
            elements = np.arange(self.min,
                                 self.max + 0.1 * step,
                                 step=step).tolist()

            elements = [round(x, self.precision) for x in elements]

        function_signature = signature(function)

        results = [0] * len(elements)

        for i in range(0, len(elements)):
            bound_params: BoundArguments = function_signature.bind(elements[i], *args, **kwargs)
            bound_params.apply_defaults()

            results[i] = function(*bound_params.args, **bound_params.kwargs)

        return Interval.infimum_supremum(min(results), max(results), precision=self.precision)

    def __add__(self, other) -> Interval:
        if isinstance(other, (float, int)):
            return Interval(self.min + other, self.max + other, precision=self.precision)
        elif isinstance(other, Interval):
            return Interval(self.min + other.min, self.max + other.max, precision=min(self.precision, other.precision))
        else:
            return NotImplemented

    def __radd__(self, other) -> Interval:
        return self + other

    def __sub__(self, other) -> Interval:
        if isinstance(other, (float, int)):
            return Interval(self.min - other, self.max - other, precision=self.precision)
        elif isinstance(other, Interval):
            return Interval(self.min - other.max, self.max - other.min, precision=min(self.precision, other.precision))
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
            return Interval(min(values), max(values), precision=min(self.precision, other.precision))
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
            
            return Interval(min(values), max(values), precision=min(self.precision, other.precision))

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

            if (power % 2) == 0:
                
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

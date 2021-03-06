from __future__ import annotations
from types import FunctionType, BuiltinFunctionType
from inspect import signature, BoundArguments
from typing import List, NoReturn
from types import FunctionType
from bisect import bisect_left
import re

from FuzzyMath.class_interval import Interval
from FuzzyMath.fuzzymath_utils import set_up_precision


class FuzzyNumber:

    __DEFAULT_PRECISION = 15

    __slots__ = ("_alpha_cuts", "_alphas", "_precision")

    def __init__(self, alphas: List[float], alpha_cuts: List[Interval], precision: int = None):

        precision = set_up_precision(precision, self.__DEFAULT_PRECISION)

        self._precision = precision

        if not isinstance(alphas, List):
            raise TypeError("`alphas` must be a list. It is `{0}`.".format(type(alphas).__name__))

        if not isinstance(alpha_cuts, List):
            raise TypeError("`alpha_cuts` must be a list. It is `{0}`.".format(type(alphas).__name__))

        if not (len(alphas) == len(alpha_cuts)):
            raise ValueError("Lists `alphas` and `alpha_cuts` must be of same length. Currently the "
                             "lengths are {0} and {1}.".format(len(alphas), len(alpha_cuts)))

        for alpha in alphas:
            if not isinstance(alpha, (int, float)):
                raise ValueError("All elements of `alphas` must be int or float.")
            if not (0 <= alpha <= 1):
                raise ValueError("All elements of `alphas` must be from range [0,1].")

        if len(alphas) != len(set(alphas)):
            raise ValueError("Values in `alphas` are not unique.")

        if 0 not in alphas or 1 not in alphas:
            raise ValueError("`alphas` must contain both 0 and 1 alpha value.")

        for alpha_cut in alpha_cuts:
            if not isinstance(alpha_cut, Interval):
                raise TypeError("All elements of `alpha_cuts` must be Interval.")

        alphas = [round(elem, self._precision) for elem in alphas]

        self._alpha_cuts = dict(zip(alphas, alpha_cuts))
        self._alphas = sorted(self._alpha_cuts.keys())

        previous_interval: Interval = Interval.empty()

        for alpha in self.alpha_levels:
            if previous_interval is not None:
                if not (self.get_alpha_cut(alpha) in previous_interval):
                    raise ValueError("Interval on lower alpha level has to contain the higher level alpha cuts."
                                     "This does not hold for {0} and {1}.".format(previous_interval,
                                                                                  self.get_alpha_cut(alpha)))

            previous_interval = self.get_alpha_cut(alpha)

        if not (self._alphas[0] == 0, self._alphas[-1] == 1):
            raise ValueError("The lowest alpha level has to be 0 and the highest alpha level has to be 1."
                             "This does not hold for {0} and {1}.".format(self._alphas[0],
                                                                          self._alphas[-1]))

    @property
    def alpha_levels(self) -> List[float]:
        return self._alphas

    @property
    def alpha_cuts(self) -> List[Interval]:
        return list(self._alpha_cuts.values())

    @property
    def min(self) -> float:
        return self.get_alpha_cut(0).min

    @property
    def max(self) -> float:
        return self.get_alpha_cut(0).max

    @property
    def kernel(self) -> Interval:
        return self.get_alpha_cut(1)

    @property
    def kernel_min(self) -> float:
        return self.kernel.min

    @property
    def kernel_max(self) -> float:
        return self.kernel.max

    def get_alpha_cut(self, alpha: float) -> Interval:
        self._validate_alpha(alpha)

        alpha = round(alpha, self._precision)

        if alpha in self.alpha_levels:
            return self._alpha_cuts.get(alpha)
        else:
            return self._calculate_alpha_cut(alpha)

    @staticmethod
    def _validate_alpha(alpha: float) -> NoReturn:
        if not isinstance(alpha, (int, float)):
            raise TypeError("`alpha` must be float or int.")

        if not (0 <= alpha <= 1):
            raise ValueError("`alpha` must be from range [0,1].")

    def _calculate_alpha_cut(self, alpha: float) -> Interval:
        position = bisect_left(self._alphas, alpha)

        x1 = self._alpha_cuts.get(self.alpha_levels[position-1]).min
        y1 = self.alpha_levels[position-1]
        x2 = self._alpha_cuts.get(self.alpha_levels[position]).min
        y2 = self.alpha_levels[position]

        if x1 == x2:
            a = x1
        else:
            k = (y1-y2) / (x1-x2)
            q = y1 - k * x1
            a = (alpha - q) / k

        x1 = self._alpha_cuts.get(self.alpha_levels[position - 1]).max
        y1 = self.alpha_levels[position-1]
        x2 = self._alpha_cuts.get(self.alpha_levels[position]).max
        y2 = self.alpha_levels[position]

        if x1 == x2:
            b = x1
        else:
            k = (y2-y1) / (x2-x1)
            q = y1 - k * x1
            b = (alpha - q) / k

        return Interval.infimum_supremum(a, b)

    def __repr__(self) -> str:
        string = ""

        for alpha in self._alphas:
            string = string + "({0};{1},{2})".format(alpha,
                                                     self.get_alpha_cut(alpha).min,
                                                     self.get_alpha_cut(alpha).max)

        return string

    def __str__(self) -> str:
        string = "Fuzzy number with support ({},{}), kernel ({}, {}) and {} more alpha-cuts.".\
            format(self.min, self.max,
                   self.kernel.min, self.kernel.max,
                   len(self.alpha_levels)-2)

        return string

    def __contains__(self, item) -> bool:
        interval = self.get_alpha_cut(0)
        if isinstance(item, (int, float)):
            return interval.min <= item <= interval.max
        elif isinstance(item, Interval):
            return interval.min <= item.min and interval.max <= self.max
        elif isinstance(item, FuzzyNumber):
            return interval.min <= item.get_alpha_cut(0).min and item.get_alpha_cut(0).max <= interval.max
        else:
            raise TypeError("Cannot test if object of type `{0}` is in FuzzyNumber. Only implemented for `float`, "
                            "`int`, `Interval` and `FuzzyNumber`.".format(type(item).__name__))

    def __lt__(self, other):
        if isinstance(other, FuzzyNumber):
            return self.max < other.min
        elif isinstance(other, (int, float)):
            return self.max < other
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, FuzzyNumber):
            return self.min > other.max
        elif isinstance(other, (int, float)):
            return self.min > other
        else:
            return NotImplemented

    @staticmethod
    def get_alpha_cut_values(number_of_parts: int, precision: int) -> List[float]:

        precision = set_up_precision(precision)

        if not isinstance(number_of_parts, int) or number_of_parts <= 1:
            raise ValueError("`number_of_cuts` has to be integer and higher than 1. "
                             "It is of type `{0}` and value `{1}`.".format(type(number_of_parts).__name__,
                                                                           number_of_parts))

        number_of_parts = int(number_of_parts)

        values = [0.0] * number_of_parts

        i = 0
        while i <= number_of_parts-1:
            values[i] = round(i/(number_of_parts-1), precision)
            i += 1

        return values

    def __add__(self, other) -> FuzzyNumber:
        if not isinstance(other, (int, float, FuzzyNumber)):
            return NotImplemented
        return self._iterate_alphas_two_values(self, other, Interval.__add__)

    def __radd__(self, other) -> FuzzyNumber:
        return self + other

    def __mul__(self, other) -> FuzzyNumber:
        if not isinstance(other, (int, float, FuzzyNumber)):
            return NotImplemented
        return self._iterate_alphas_two_values(self, other, Interval.__mul__)

    def __rmul__(self, other) -> FuzzyNumber:
        return self * other

    def __sub__(self, other) -> FuzzyNumber:
        if not isinstance(other, (int, float, FuzzyNumber)):
            return NotImplemented
        return self._iterate_alphas_two_values(self, other, Interval.__sub__)

    def __rsub__(self, other) -> FuzzyNumber:
        if not isinstance(other, (int, float, FuzzyNumber)):
            return NotImplemented
        return self._iterate_alphas_two_values(self, other, Interval.__rsub__)

    def __truediv__(self, other) -> FuzzyNumber:
        if not isinstance(other, (int, float, FuzzyNumber)):
            return NotImplemented

        if isinstance(other, FuzzyNumber):
            if 0 in other:
                raise ArithmeticError("Cannot divide by FuzzyNumber that contains 0.")

        if isinstance(other, (int, float)) and other == 0:
            raise ArithmeticError("Cannot divide by 0.")

        return self._iterate_alphas_two_values(self, other, Interval.__truediv__)

    def __rtruediv__(self, other) -> FuzzyNumber:
        if not isinstance(other, (int, float, FuzzyNumber)):
            return NotImplemented

        if 0 in self:
            raise ArithmeticError("Cannot divide by FuzzyNumber that contains 0.")

        return self._iterate_alphas_two_values(self, other, Interval.__rtruediv__)

    def __pow__(self, power) -> FuzzyNumber:
        return self._iterate_alphas_one_value(self, Interval.__pow__, power)

    def __hash__(self) -> int:
        list_values = [None] * (len(self.alpha_levels) * 2)
        i = 0
        for alpha in self.alpha_levels:
            interval = self.get_alpha_cut(alpha)
            list_values[i] = interval.min
            list_values[i+1] = interval.max
            i += 2
        return hash(tuple(list_values))

    def __eq__(self, other) -> bool:
        if isinstance(other, FuzzyNumber):
            alpha_levels = self.alpha_levels == other.alpha_levels
            alpha_cuts = list(self.alpha_cuts) == list(other.alpha_cuts)
            precision = self._precision == other._precision

            return alpha_levels and alpha_cuts and precision
        else:
            return NotImplemented

    def __len__(self) -> int:
        return len(self.alpha_cuts)

    def possibility_exceedance(self, fn_other: FuzzyNumber) -> float:
        from FuzzyMath.fuzzynumber_comparisons import possibility_exceedance
        return possibility_exceedance(self, fn_other)

    def necessity_exceedance(self, fn_other: FuzzyNumber) -> float:
        from FuzzyMath.fuzzynumber_comparisons import necessity_exceedance
        return necessity_exceedance(self, fn_other)

    def possibility_strict_exceedance(self, fn_other: FuzzyNumber) -> float:
        from FuzzyMath.fuzzynumber_comparisons import possibility_strict_exceedance
        return possibility_strict_exceedance(self, fn_other)

    def necessity_strict_exceedance(self, fn_other: FuzzyNumber) -> float:
        from FuzzyMath.fuzzynumber_comparisons import necessity_strict_exceedance
        return necessity_strict_exceedance(self, fn_other)

    def possibility_undervaluation(self, fn_other: FuzzyNumber) -> float:
        from FuzzyMath.fuzzynumber_comparisons import possibility_undervaluation
        return possibility_undervaluation(self, fn_other)

    def necessity_undervaluation(self, fn_other: FuzzyNumber) -> float:
        from FuzzyMath.fuzzynumber_comparisons import necessity_undervaluation
        return necessity_undervaluation(self, fn_other)

    def possibility_strict_undervaluation(self, fn_other: FuzzyNumber) -> float:
        from FuzzyMath.fuzzynumber_comparisons import possibility_strict_undervaluation
        return possibility_strict_undervaluation(self, fn_other)

    def necessity_strict_undervaluation(self, fn_other: FuzzyNumber) -> float:
        from FuzzyMath.fuzzynumber_comparisons import necessity_strict_undervaluation
        return necessity_strict_undervaluation(self, fn_other)

    def apply_function(self,
                       function: (FunctionType, BuiltinFunctionType),
                       *args,
                       monotone: bool = False,
                       number_elements: float = 1000,
                       **kwargs) -> FuzzyNumber:

        intervals = []

        alpha_levels = list(self.alpha_levels)
        alpha_levels.reverse()

        width = self.max - self.min

        i = 0
        for alpha in alpha_levels:

            alpha_width = self.get_alpha_cut(alpha).max - self.get_alpha_cut(alpha).min

            number_elements_cut = (alpha_width/width)*number_elements

            interval = self.get_alpha_cut(alpha).apply_function(function,
                                                                *args,
                                                                monotone=monotone,
                                                                number_elements=number_elements_cut,
                                                                **kwargs)

            if i != 0:
                interval = interval.union_hull(intervals[i-1])

            intervals.append(interval)
            i += 1

        intervals.reverse()

        return FuzzyNumber(self.alpha_levels, intervals, precision=self._precision)

    @staticmethod
    def _iterate_alphas_one_value(x, operation: FunctionType, *args) -> FuzzyNumber:
        if not isinstance(operation, FunctionType):
            raise TypeError("`operation` needs to be a function. It is `{0}`."
                            .format(type(operation).__name__))
        alphas, intervals = FuzzyNumber.__prepare_alphas_intervals(x.alpha_levels)

        i = 0
        for alpha in alphas:
            intervals[i] = operation(x.get_alpha_cut(alpha), *args)
            i += 1

        return FuzzyNumber(alphas, intervals, precision=x._precision)

    @staticmethod
    def _iterate_alphas_two_values(x, y, operation: FunctionType) -> FuzzyNumber:

        if not isinstance(operation, FunctionType):
            raise TypeError("`operation` needs to be a function. It is `{0}`."
                            .format(type(operation).__name__))

        fuzzy_x = isinstance(x, FuzzyNumber)
        fuzzy_y = isinstance(y, FuzzyNumber)

        if fuzzy_x and fuzzy_y:
            alphas, intervals = FuzzyNumber.__prepare_alphas_intervals(x.alpha_levels, y.alpha_levels)
            precision = x._precision
        elif fuzzy_x:
            alphas, intervals = FuzzyNumber.__prepare_alphas_intervals(x.alpha_levels)
            precision = x._precision
        elif fuzzy_y:
            alphas, intervals = FuzzyNumber.__prepare_alphas_intervals(y.alpha_levels)
            precision = y._precision
        else:
            raise RuntimeError("At least one argument has to be `FuzzyNumber`.")

        i = 0
        for alpha in alphas:
            if fuzzy_x and fuzzy_y:
                intervals[i] = operation(x.get_alpha_cut(alpha), y.get_alpha_cut(alpha))
            elif fuzzy_x:
                intervals[i] = operation(x.get_alpha_cut(alpha), y)
            elif fuzzy_y:
                intervals[i] = operation(x, y.get_alpha_cut(alpha))
            i += 1

        return FuzzyNumber(alphas, intervals, precision=precision)

    def __get_cuts_values(self,
                          alphas: List[float] = None,
                          order_by_alphas_from_one: bool = False,
                          value_type: str = "min") -> List[float]:
        if alphas is None:
            alphas = self.alpha_levels
        else:
            alphas.sort()

        values = [0] * len(alphas)

        for i in range(len(alphas)):

            if value_type == "min":
                values[i] = self.get_alpha_cut(alphas[i]).min

            elif value_type == "max":
                values[i] = self.get_alpha_cut(alphas[i]).max

        if order_by_alphas_from_one:
            values.reverse()

        return values

    def get_alpha_cuts_mins(self,
                            alphas: List[float] = None,
                            order_by_alphas_from_one: bool = False) -> List[float]:

        return self.__get_cuts_values(alphas=alphas,
                                      order_by_alphas_from_one=order_by_alphas_from_one,
                                      value_type="min")

    def get_alpha_cuts_maxs(self,
                            alphas: List[float] = None,
                            order_by_alphas_from_one: bool = False) -> List[float]:

        return self.__get_cuts_values(alphas=alphas,
                                      order_by_alphas_from_one=order_by_alphas_from_one,
                                      value_type="max")

    @staticmethod
    def _prepare_alphas(alpha_levels1: List[float],
                        alpha_levels2: List[float]):

        alphas = sorted(list(set.union(set(alpha_levels1), set(alpha_levels2))))
        return alphas

    @staticmethod
    def __prepare_alphas_intervals(alpha_levels1: List[float],
                                   alpha_levels2: List[float] = None) -> (List[float], List[Interval]):
        if alpha_levels2 is None:
            alphas = list(set(alpha_levels1))
        else:
            alphas = list(set.union(set(alpha_levels1), set(alpha_levels2)))

        alphas = sorted(alphas)
        intervals = [Interval.empty()] * len(alphas)

        return alphas, intervals

    @classmethod
    def triangular(cls,
                   minimum: float, kernel: float, maximum: float,
                   number_of_cuts: int = None,
                   precision: int = None) -> FuzzyNumber:

        if not minimum <= kernel <= maximum:
            raise ValueError("The fuzzy number is invalid. The structure needs to be `minimum` <= `kernel` "
                             "<= `maximum`. Currently it is `{0}` <= `{1}` <= `{2}`, which does not hold."
                             .format(minimum, kernel, maximum))

        precision = set_up_precision(precision)

        if number_of_cuts is None or number_of_cuts <= 2:

            return cls(alphas=[0, 1],
                       alpha_cuts=[Interval.infimum_supremum(minimum, maximum, precision=precision),
                                   Interval.infimum_supremum(kernel, kernel, precision=precision)],
                       precision=precision)

        else:
            alphas = FuzzyNumber.get_alpha_cut_values(number_of_cuts, precision)

            intervals = [Interval.empty()] * len(alphas)

            i = 0
            for alpha in alphas:
                if alpha == 0:
                    intervals[i] = Interval.infimum_supremum(minimum, maximum, precision=precision)
                elif alpha == 1:
                    intervals[i] = Interval.infimum_supremum(kernel, kernel, precision=precision)
                else:
                    int_min = ((kernel - minimum) / (number_of_cuts - 1)) * i + minimum
                    int_max = maximum - ((maximum - kernel) / (number_of_cuts - 1)) * i
                    intervals[i] = Interval.infimum_supremum(int_min, int_max, precision=precision)
                i += 1

            return cls(alphas=alphas,
                       alpha_cuts=intervals,
                       precision=precision)

    @classmethod
    def trapezoidal(cls,
                    minimum: float, kernel_minimum: float, kernel_maximum: float, maximum: float,
                    number_of_cuts: int = None,
                    precision: int = None) -> FuzzyNumber:

        if not minimum <= kernel_minimum <= kernel_maximum <= maximum:
            raise ValueError("The fuzzy number is invalid. The structure needs to be "
                             "`minimum` <= `kernel_minimum` <= `kernel_maximum` <= `maximum`. "
                             "Currently it is `{0}` <= `{1}` <= `{2}` <= `{3}`, which does not hold."
                             .format(minimum, kernel_minimum, kernel_maximum, maximum))

        precision = set_up_precision(precision)

        if number_of_cuts is None or number_of_cuts <= 2:

            return cls(alphas=[0, 1],
                       alpha_cuts=[Interval.infimum_supremum(minimum, maximum, precision=precision),
                                   Interval.infimum_supremum(kernel_minimum, kernel_maximum, precision=precision)],
                       precision=precision)

        else:
            alphas = FuzzyNumber.get_alpha_cut_values(number_of_cuts, precision)

            intervals = [Interval.empty()] * len(alphas)

            i = 0
            for alpha in alphas:
                if alpha == 0:
                    intervals[i] = Interval.infimum_supremum(minimum, maximum, precision=precision)
                elif alpha == 1:
                    intervals[i] = Interval.infimum_supremum(kernel_minimum, kernel_maximum, precision=precision)
                else:
                    int_min = ((kernel_minimum - minimum) / (number_of_cuts - 1)) * i + minimum
                    int_max = maximum - ((maximum - kernel_maximum) / (number_of_cuts - 1)) * i
                    intervals[i] = Interval.infimum_supremum(int_min, int_max, precision=precision)
                i += 1

            return cls(alphas=alphas,
                       alpha_cuts=intervals,
                       precision=precision)

    @classmethod
    def crisp_number(cls,
                     value: float,
                     precision: int = None) -> FuzzyNumber:

        precision = set_up_precision(precision)

        return cls(alphas=[0, 1],
                   alpha_cuts=[Interval.infimum_supremum(value, value, precision=precision),
                               Interval.infimum_supremum(value, value, precision=precision)],
                   precision=precision)

    @classmethod
    def parse_string(cls,
                     string: str,
                     precision: int = None) -> FuzzyNumber:

        precision = set_up_precision(precision)

        re_a_cuts = re.compile("([0-9\.;,]+)")
        re_numbers = re.compile("[0-9\.]+")

        elements = re_a_cuts.findall(string)

        alphas: List[float] = [0] * len(elements)
        alpha_cuts: List[Interval] = [Interval.empty()] * len(elements)

        i: int = 0

        for a_cut_def in elements:

            numbers = re_numbers.findall(a_cut_def)

            if len(numbers) != 3:
                raise ValueError("Cannot parse FuzzyNumber from this definition. "
                                 "Not all elements provide 3 values (alpha cut value and interval).")

            numbers = [float(x) for x in numbers]

            try:
                cls._validate_alpha(numbers[0])
            except ValueError as err:
                raise ValueError("`{}` element of Fuzzy Number is incorrectly defiend. {}".format(a_cut_def, err))

            alphas[i] = numbers[0]

            try:
                alpha_cuts[i] = Interval.infimum_supremum(numbers[1], numbers[2])
            except ValueError as err:
                raise ValueError("`{}` element of Fuzzy Number is incorrectly defiend. {}".format(a_cut_def, err))

            i += 1

        return FuzzyNumber(alphas, alpha_cuts, precision)

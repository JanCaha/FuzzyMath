from FuzzyMath.class_interval import Interval
from typing import List
from types import FunctionType
from bisect import bisect_left
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
            if not (0 <= alpha <= 1) and not isinstance(alpha, (int, float)):
                raise ValueError("All elements of `alphas` must be int or float from range [0,1].")

        if len(alphas) != len(set(alphas)):
            raise ValueError("Values in `alphas` are not unique.")

        for alpha_cut in alpha_cuts:
            if not isinstance(alpha_cut, Interval):
                raise TypeError("All elements of `alpha_cuts` must be Interval.")

        alphas = [round(elem, self._precision) for elem in alphas]

        self._alpha_cuts = dict(zip(alphas, alpha_cuts))
        self._alphas = sorted(self._alpha_cuts.keys())

        previous_interval: Interval = None

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
    def alpha_levels(self):
        return self._alphas

    @property
    def alpha_cuts(self):
        return self._alpha_cuts.values()

    def get_alpha_cut(self, alpha: float):
        self._validate_alpha(alpha)

        alpha = round(alpha, self._precision)

        if alpha in self.alpha_levels:
            return self._alpha_cuts.get(alpha)
        else:
            return self._calculate_alpha_cut(alpha)

    @staticmethod
    def _validate_alpha(alpha: float):
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
            k = (y2-y1) / (x2-x1);
            q = y1 - k * x1;
            b = (alpha - q) / k;

        return Interval.infimum_supremum(a, b)

    def __repr__(self):
        string = ""

        for alpha in self._alphas:
            string = string + "({0};{1},{2})".format(alpha,
                                                     self.get_alpha_cut(alpha).min,
                                                     self.get_alpha_cut(alpha).max)

        return string

    def __contains__(self, item):
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

    @staticmethod
    def get_alpha_cut_values(number_of_parts: int, precision: int) -> List[float]:

        precision = set_up_precision(precision)

        if not isinstance(number_of_parts, int) or number_of_parts <= 1:
            raise ValueError("`number_of_cuts` has to be integer and higher than 1. "
                             "It is of type `{0}` and value `{1}`.".format(type(number_of_parts).__name__,
                                                                           number_of_parts))

        number_of_parts = int(number_of_parts)

        values = [None] * number_of_parts

        i = 0
        while i <= number_of_parts-1:
            values[i] = round(i/(number_of_parts-1), precision)
            i += 1

        return values

    def __add__(self, other):
        if not isinstance(other, (int, float, FuzzyNumber)):
            return NotImplemented
        return self._iterate_alphas_two_values(self, other, Interval.__add__)

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        if not isinstance(other, (int, float, FuzzyNumber)):
            return NotImplemented
        return self._iterate_alphas_two_values(self, other, Interval.__mul__)

    def __rmul__(self, other):
        return self * other

    def __sub__(self, other):
        if not isinstance(other, (int, float, FuzzyNumber)):
            return NotImplemented
        return self._iterate_alphas_two_values(self, other, Interval.__sub__)

    def __rsub__(self, other):
        if not isinstance(other, (int, float, FuzzyNumber)):
            return NotImplemented
        return self._iterate_alphas_two_values(self, other, Interval.__rsub__)

    def __truediv__(self, other):
        if not isinstance(other, (int, float, FuzzyNumber)):
            return NotImplemented

        if isinstance(other, FuzzyNumber):
            if 0 in other:
                raise ArithmeticError("Cannot divide by FuzzyNumber that contains 0.")

        return self._iterate_alphas_two_values(self, other, Interval.__truediv__)

    def __rtruediv__(self, other):
        if not isinstance(other, (int, float, FuzzyNumber)):
            return NotImplemented

        if 0 in self:
            raise ArithmeticError("Cannot divide by FuzzyNumber that contains 0.")

        return self._iterate_alphas_two_values(self, other, Interval.__rtruediv__)

    def __pow__(self, power):
        return self._iterate_alphas_one_value(self, Interval.__pow__, power)

    def __hash__(self):
        list_values = [None] * (len(self.alpha_levels) * 2)
        i = 0
        for alpha in self.alpha_levels:
            interval = self.get_alpha_cut(alpha)
            list_values[i] = interval.min
            list_values[i+1] = interval.max
            i += 2
        return hash(tuple(list_values))



    @staticmethod
    def _iterate_alphas_one_value(x, operation: FunctionType, *args):
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
    def _iterate_alphas_two_values(x, y, operation: FunctionType):

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

    @staticmethod
    def __prepare_alphas_intervals(alpha_levels1: List[float],
                                   alpha_levels2: List[float] = None) -> (List[float], List[Interval]):
        if alpha_levels2 is None:
            alphas = list(set(alpha_levels1))
        else:
            alphas = list(set.union(set(alpha_levels1), set(alpha_levels2)))

        alphas = sorted(alphas)
        intervals = [None] * len(alphas)

        return alphas, intervals

    @classmethod
    def triangular(cls,
                   minimum: float, kernel: float, maximum: float,
                   number_of_cuts: int = None,
                   precision: int = None):

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

            intervals = [None] * len(alphas)

            i = 0
            for alpha in alphas:
                if alpha == 0:
                    intervals[i] = Interval.infimum_supremum(minimum, maximum, precision=precision)
                elif alpha == 1:
                    intervals[i] = Interval.infimum_supremum(kernel, kernel, precision=precision)
                else:
                    int_min = ((kernel - minimum) / number_of_cuts) * i + minimum
                    int_max = maximum - ((maximum - kernel) / number_of_cuts) * i
                    intervals[i] = Interval.infimum_supremum(int_min, int_max, precision=precision)
                i += 1

            return cls(alphas=alphas,
                       alpha_cuts=intervals,
                       precision=precision)

    @classmethod
    def trapezoidal(cls,
                    minimum: float, kernel_minimum: float, kernel_maximum: float, maximum: float,
                    number_of_cuts: int = None,
                    precision: int = None):

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

            intervals = [None] * len(alphas)

            i = 0
            for alpha in alphas:
                if alpha == 0:
                    intervals[i] = Interval.infimum_supremum(minimum, maximum, precision=precision)
                elif alpha == 1:
                    intervals[i] = Interval.infimum_supremum(kernel_minimum, kernel_maximum, precision=precision)
                else:
                    int_min = ((kernel_minimum - minimum) / number_of_cuts) * i + minimum
                    int_max = maximum - ((maximum - kernel_maximum) / number_of_cuts) * i
                    intervals[i] = Interval.infimum_supremum(int_min, int_max, precision=precision)
                i += 1

            return cls(alphas=alphas,
                       alpha_cuts=intervals,
                       precision=precision)

    @classmethod
    def crisp_number(cls,
                     value: float,
                     precision: int = None):

        precision = set_up_precision(precision)

        return cls(alphas=[0, 1],
                   alpha_cuts=[Interval.infimum_supremum(value, value, precision=precision),
                               Interval.infimum_supremum(value, value, precision=precision)],
                   precision=precision)

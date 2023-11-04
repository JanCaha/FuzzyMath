from __future__ import annotations

from bisect import bisect_left
from decimal import Decimal, InvalidOperation
from types import BuiltinFunctionType, FunctionType
from typing import Callable, List, Tuple, Union

from .class_interval import Interval
from .class_memberships import FuzzyMembership, PossibilisticMembership


class FuzzyNumber:
    """
    Fuzzy number representation.
    ...
    Attributes
    ----------
    _alpha_cuts: List[Interval]
        List of Intervals representing alpha cuts.

    _alphas: List[float]
        List of alpha values.
    """

    __slots__ = ("_alpha_cuts", "_alphas")

    def __init__(self, alphas: List[float], alpha_cuts: List[Interval]):
        """
        Basic creator for the class. But generally it is more useful to use functions `FuzzyNumberFactory.triangular()`,
        `FuzzyNumberFactory.trapezoidal()`, `FuzzyNumberFactory.crisp_number()` or `FuzzyNumberFactory.parse_string()` instead of this
        function.

        Parameters
        ----------
        alphas: List[float]
        alpha_cuts: List[Interval]
        """

        if not isinstance(alphas, List):
            raise TypeError("`alphas` must be a list. It is `{0}`.".format(type(alphas).__name__))

        if not isinstance(alpha_cuts, List):
            raise TypeError("`alpha_cuts` must be a list. It is `{0}`.".format(type(alphas).__name__))

        if not (len(alphas) == len(alpha_cuts)):
            raise ValueError(
                "Lists `alphas` and `alpha_cuts` must be of same length. Currently the "
                "lengths are {0} and {1}.".format(len(alphas), len(alpha_cuts))
            )

        for i, alpha in enumerate(alphas):
            alphas[i] = self._validate_alpha(alpha)

        if len(alphas) != len(set(alphas)):
            raise ValueError("Values in `alphas` are not unique.")

        if 0 not in alphas or 1 not in alphas:
            raise ValueError("`alphas` must contain both 0 and 1 alpha value.")

        for alpha_cut in alpha_cuts:
            if not isinstance(alpha_cut, Interval):
                raise TypeError("All elements of `alpha_cuts` must be Interval.")

        self._alpha_cuts = dict(zip(alphas, alpha_cuts))
        self._alphas = sorted(self._alpha_cuts.keys())

        previous_interval: Interval = Interval(float("nan"), float("nan"))

        for alpha in self.alpha_levels:
            if not previous_interval.is_empty:
                if not (self.get_alpha_cut(alpha) in previous_interval):
                    raise ValueError(
                        "Interval on lower alpha level has to contain the higher level alpha cuts."
                        "This does not hold for {0} and {1}.".format(previous_interval, self.get_alpha_cut(alpha))
                    )

            previous_interval = self.get_alpha_cut(alpha)

        if not (self._alphas[0] == 0, self._alphas[-1] == 1):
            raise ValueError(
                "The lowest alpha level has to be 0 and the highest alpha level has to be 1."
                "This does not hold for {0} and {1}.".format(self._alphas[0], self._alphas[-1])
            )

    @property
    def alpha_levels(self) -> List[float]:
        """
        Alpha levels for this fuzzy number.

        Returns
        -------
        List[float]
        """
        return self._alphas

    @property
    def alpha_cuts(self) -> List[Interval]:
        """
        Alpha cuts (intervals) for this fuzzy number.

        Returns
        -------
        List[Interval]
        """
        return list(self._alpha_cuts.values())

    @property
    def min(self) -> float:
        """
        Minimal value of this fuzzy number.

        Returns
        -------
        float
        """
        return self.get_alpha_cut(0).min

    @property
    def max(self) -> float:
        """
        Maximal value of this fuzzy number.

        Returns
        -------
        float
        """
        return self.get_alpha_cut(0).max

    @property
    def kernel(self) -> Interval:
        """
        Kernel (alpha cut with membership value 1) for this fuzzy number.

        Returns
        -------
        Interval
        """
        return self.get_alpha_cut(1)

    @property
    def kernel_min(self) -> float:
        """
        Minimal kernel value of this fuzzy number.

        Returns
        -------
        float
        """
        return self.kernel.min

    @property
    def kernel_max(self) -> float:
        """
        Maximal kernel value of this fuzzy number.

        Returns
        -------
        float
        """
        return self.kernel.max

    def get_alpha_cut(self, alpha: Union[str, int, float, Decimal]) -> Interval:
        """
        Extracts alpha cut specified by `alpha` variable.

        Parameters
        ----------
        alpha: Union[str, int, float, Decimal]
            Value of alpha to extract alpha cut for. Must be from range [0, 1].

        Returns
        -------
        Interval
        """

        alpha = self._validate_alpha(alpha)

        if alpha in self.alpha_levels:
            return self._alpha_cuts.get(alpha)
        else:
            return self._calculate_alpha_cut(alpha)

    @staticmethod
    def _validate_alpha(alpha: Union[str, int, float, Decimal]) -> Decimal:
        """
        Validates value of of alpha. Must be from range [0, 1].

        Parameters
        ----------
        alpha: Union[str, int, float, Decimal]
            Alpha to validate.

        Raises
        -------
        ValueError
            If `alpha` is not from range [0, 1].
        TypeError
            If `alpha` is not int or float.

        Returns
        -------
        Decimal
        """

        if not isinstance(alpha, (str, int, float, Decimal)):
            raise TypeError("`alpha` must be Decimal, int, float or str.")

        if not isinstance(alpha, Decimal):
            try:
                alpha = Decimal(alpha)
            except InvalidOperation as e:
                raise InvalidOperation(f"Cannot convert alpha value `{alpha}` to number.") from e

        if not (0 <= alpha <= 1):
            raise ValueError("`alpha` must be from range [0,1].")

        return alpha

    def _calculate_alpha_cut(self, alpha: float) -> Interval:
        """
        Calculates alpha cut for given alpha.

        Parameters
        ----------
        alpha: float
            Alpha to calculate the alpha cut for.

        Returns
        -------
        Interval
        """

        position = bisect_left(self._alphas, alpha)

        x1 = self._alpha_cuts.get(self.alpha_levels[position - 1]).min
        y1 = self.alpha_levels[position - 1]
        x2 = self._alpha_cuts.get(self.alpha_levels[position]).min
        y2 = self.alpha_levels[position]

        if x1 == x2:
            a = x1
        else:
            k = (y1 - y2) / (x1 - x2)
            q = y1 - k * x1
            a = (Decimal(alpha) - q) / k

        x1 = self._alpha_cuts.get(self.alpha_levels[position - 1]).max
        y1 = self.alpha_levels[position - 1]
        x2 = self._alpha_cuts.get(self.alpha_levels[position]).max
        y2 = self.alpha_levels[position]

        if x1 == x2:
            b = x1
        else:
            k = (y2 - y1) / (x2 - x1)
            q = y1 - k * x1
            b = (Decimal(alpha) - q) / k

        return Interval(min(a, b), max(a, b))

    def __repr__(self) -> str:
        """
        Complete representation of fuzzy number.

        Returns
        -------
        str
        """

        string = ""

        for alpha in self._alphas:
            string = string + "({0};{1},{2})".format(
                alpha, self.get_alpha_cut(alpha).min, self.get_alpha_cut(alpha).max
            )

        return string

    def __str__(self) -> str:
        """
        Simplified representation of fuzzy number.

        Returns
        -------
        str
        """

        string = "Fuzzy number with support ({},{}), kernel ({}, {}) and {} more alpha-cuts.".format(
            self.min, self.max, self.kernel.min, self.kernel.max, len(self.alpha_levels) - 2
        )

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
            raise TypeError(
                "Cannot test if object of type `{0}` is in FuzzyNumber. Only implemented for `float`, "
                "`int`, `Interval` and `FuzzyNumber`.".format(type(item).__name__)
            )

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
    def get_alpha_cut_values(number_of_parts: int) -> List[Decimal]:
        """
        Returns alpha cut values for given number of parts.

        Parameters
        ----------
        number_of_parts: int
            Number of alpha cuts to be returned.

        Returns
        -------
        List[Decimal]
            List of Decimal representing alphas.
        """

        if not isinstance(number_of_parts, int) or number_of_parts <= 1:
            raise ValueError(
                "`number_of_cuts` has to be integer and higher than 1. "
                "It is of type `{0}` and value `{1}`.".format(type(number_of_parts).__name__, number_of_parts)
            )

        number_of_parts = int(number_of_parts)

        values = [0.0] * number_of_parts

        i = 0
        while i <= number_of_parts - 1:
            values[i] = Decimal(i) / (Decimal(number_of_parts) - Decimal(1))
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
        list_values = [0.0] * (len(self.alpha_levels) * 2)
        i = 0
        for alpha in self.alpha_levels:
            interval = self.get_alpha_cut(alpha)
            list_values[i] = interval.min
            list_values[i + 1] = interval.max
            i += 2
        return hash(tuple(list_values))

    def __eq__(self, other) -> bool:
        if isinstance(other, FuzzyNumber):
            alpha_levels = self.alpha_levels == other.alpha_levels
            alpha_cuts = list(self.alpha_cuts) == list(other.alpha_cuts)

            return alpha_levels and alpha_cuts
        else:
            return NotImplemented

    def __len__(self) -> int:
        return len(self.alpha_cuts)

    def possibility_exceedance(self, fn_other: FuzzyNumber) -> Decimal:
        from .fuzzynumber_comparisons import possibility_exceedance

        return possibility_exceedance(self, fn_other)

    def necessity_exceedance(self, fn_other: FuzzyNumber) -> Decimal:
        from .fuzzynumber_comparisons import necessity_exceedance

        return necessity_exceedance(self, fn_other)

    def exceedance(self, fn_other: FuzzyNumber) -> PossibilisticMembership:
        from .fuzzynumber_comparisons import exceedance

        return exceedance(self, fn_other)

    def possibility_strict_exceedance(self, fn_other: FuzzyNumber) -> Decimal:
        from .fuzzynumber_comparisons import possibility_strict_exceedance

        return possibility_strict_exceedance(self, fn_other)

    def necessity_strict_exceedance(self, fn_other: FuzzyNumber) -> Decimal:
        from .fuzzynumber_comparisons import necessity_strict_exceedance

        return necessity_strict_exceedance(self, fn_other)

    def strict_exceedance(self, fn_other: FuzzyNumber) -> PossibilisticMembership:
        from .fuzzynumber_comparisons import strict_exceedance

        return strict_exceedance(self, fn_other)

    def possibility_undervaluation(self, fn_other: FuzzyNumber) -> Decimal:
        from .fuzzynumber_comparisons import possibility_undervaluation

        return possibility_undervaluation(self, fn_other)

    def necessity_undervaluation(self, fn_other: FuzzyNumber) -> Decimal:
        from .fuzzynumber_comparisons import necessity_undervaluation

        return necessity_undervaluation(self, fn_other)

    def undervaluation(self, fn_other: FuzzyNumber) -> PossibilisticMembership:
        from .fuzzynumber_comparisons import undervaluation

        return undervaluation(self, fn_other)

    def possibility_strict_undervaluation(self, fn_other: FuzzyNumber) -> Decimal:
        from .fuzzynumber_comparisons import possibility_strict_undervaluation

        return possibility_strict_undervaluation(self, fn_other)

    def necessity_strict_undervaluation(self, fn_other: FuzzyNumber) -> Decimal:
        from .fuzzynumber_comparisons import necessity_strict_undervaluation

        return necessity_strict_undervaluation(self, fn_other)

    def strict_undervaluation(self, fn_other: FuzzyNumber) -> PossibilisticMembership:
        from .fuzzynumber_comparisons import strict_undervaluation

        return strict_undervaluation(self, fn_other)

    def apply_function(
        self, function: Callable, *args, monotone: bool = False, number_elements: int = 1000, **kwargs
    ) -> FuzzyNumber:
        """
        Apply mathematical function to fuzzy number.

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
        FuzzyNumber
            New `FuzzyNumber`.
        """

        if not isinstance(function, (FunctionType, BuiltinFunctionType)):
            raise ValueError(
                "`function` must be either `FunctionType` or `BuiltinFunctionType`. `function` currently "
                "is `{}`.".format(type(function))
            )

        if not isinstance(number_elements, (int, float)):
            raise ValueError(
                "`number_elements` must be either `int` or `float`. `number_elements` is currently "
                "`{}`.".format(type(number_elements))
            )

        if not isinstance(monotone, bool):
            raise ValueError("`monotone` must be `bool`. `monotone` is currently `{}`.".format(monotone))

        intervals: List[Interval] = []

        alpha_levels = list(self.alpha_levels)
        alpha_levels.reverse()

        width = self.max - self.min

        i = 0
        for alpha in alpha_levels:
            alpha_width = self.get_alpha_cut(alpha).max - self.get_alpha_cut(alpha).min

            number_elements_cut = (alpha_width / width) * number_elements

            interval = self.get_alpha_cut(alpha).apply_function(
                function, *args, monotone=monotone, number_elements=number_elements_cut, **kwargs
            )

            if i != 0:
                interval = interval.union_hull(intervals[i - 1])

            intervals.append(interval)
            i += 1

        intervals.reverse()

        return FuzzyNumber(self.alpha_levels, intervals)

    @staticmethod
    def _iterate_alphas_one_value(x: FuzzyNumber, operation: Callable, *args) -> FuzzyNumber:
        if not callable(operation):
            raise TypeError("`operation` needs to be a function. It is `{0}`.".format(type(operation).__name__))

        alphas, intervals = FuzzyNumber.__prepare_alphas_intervals(x.alpha_levels)

        i = 0

        for alpha in alphas:
            intervals[i] = operation(x.get_alpha_cut(alpha), *args)
            i += 1

        return FuzzyNumber(alphas, intervals)

    @staticmethod
    def _iterate_alphas_two_values(x, y, operation: Callable) -> FuzzyNumber:
        if not isinstance(operation, FunctionType):
            raise TypeError("`operation` needs to be a function. It is `{0}`.".format(type(operation).__name__))

        fuzzy_x = isinstance(x, FuzzyNumber)
        fuzzy_y = isinstance(y, FuzzyNumber)

        if fuzzy_x and fuzzy_y:
            alphas, intervals = FuzzyNumber.__prepare_alphas_intervals(x.alpha_levels, y.alpha_levels)
        elif fuzzy_x:
            alphas, intervals = FuzzyNumber.__prepare_alphas_intervals(x.alpha_levels)
        elif fuzzy_y:
            alphas, intervals = FuzzyNumber.__prepare_alphas_intervals(y.alpha_levels)
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

        return FuzzyNumber(alphas, intervals)

    def __get_cuts_values(
        self, alphas: List[Decimal] = None, order_by_alphas_from_one: bool = False, value_type: str = "min"
    ) -> List[Decimal]:
        if alphas is None:
            alphas = self.alpha_levels
        else:
            alphas.sort()

        values = [0.0] * len(alphas)

        for i in range(len(alphas)):
            if value_type == "min":
                values[i] = self.get_alpha_cut(alphas[i]).min

            elif value_type == "max":
                values[i] = self.get_alpha_cut(alphas[i]).max

        if order_by_alphas_from_one:
            values.reverse()

        return values

    def get_alpha_cuts_mins(self, alphas: List[float] = None, order_by_alphas_from_one: bool = False) -> List[float]:
        """
        Extract minimimal values of provided alpha cuts as list.

        Parameters
        ----------
        alphas: List[float]
            Alphas to extract values for.

        order_by_alphas_from_one: bool
            Order alphas from one (highest) to zero (lowest)? Default is `False`, which means that ordering is lowest
            (0) to highest (1).

        Returns
        -------
        List[float]
        """
        return self.__get_cuts_values(
            alphas=alphas, order_by_alphas_from_one=order_by_alphas_from_one, value_type="min"
        )

    def get_alpha_cuts_maxs(self, alphas: List[float] = None, order_by_alphas_from_one: bool = False) -> List[float]:
        """
        Extract maximal values of provided alpha cuts as list.

        Parameters
        ----------
        alphas: List[float]
            Alphas to extract values for.

        order_by_alphas_from_one: bool
            Order alphas from one (highest) to zero (lowest)? Default is `False`, which means that ordering is lowest
            (0) to highest (1).

        Returns
        -------
        List[float]
        """
        return self.__get_cuts_values(
            alphas=alphas, order_by_alphas_from_one=order_by_alphas_from_one, value_type="max"
        )

    @staticmethod
    def _prepare_alphas(alpha_levels1: List[float], alpha_levels2: List[float]) -> List[float]:
        """
        Prepares list of alphas based on two input lists of alphas by selecting only distinct alpha values.

        Parameters
        ----------
        alpha_levels1: List[float]
        alpha_levels2: List[float]

        Returns
        -------
        List[float]
        """
        alphas = sorted(list(set.union(set(alpha_levels1), set(alpha_levels2))))
        return alphas

    @staticmethod
    def __prepare_alphas_intervals(
        alpha_levels1: List[float], alpha_levels2: List[float] = None
    ) -> Tuple[List[float], List[Interval]]:
        """
        Prepares list of alphas and list of empty `Interval`s for provided alpha levels.

        Parameters
        ----------
        alpha_levels1: List[float]
        alpha_levels2: List[float]

        Returns
        -------
        (List[float], List[Interval])
            List of alpha values and list of empty intervals prepared for further use.
        """

        if alpha_levels2 is None:
            alphas = sorted(list(set(alpha_levels1)))
        else:
            alphas = FuzzyNumber._prepare_alphas(alpha_levels1, alpha_levels2)

        intervals = [Interval(float("nan"), float("nan"))] * len(alphas)

        return alphas, intervals

    def membership(self, value: Union[float, int]) -> FuzzyMembership:
        if not isinstance(value, (int, float)):
            raise TypeError(
                "Cannot get membership of `{0}` in FuzzyNumber. Only implemented for `float`, "
                "`int`.".format(type(value).__name__)
            )

        if value not in self:
            return FuzzyMembership(0)

        elif self.kernel_min <= value <= self.kernel_max:
            return FuzzyMembership(1)

        else:
            last_alpha_containing = int(0)

            for i in range(len(self)):
                if value in self.alpha_cuts[i]:
                    last_alpha_containing = i
                else:
                    break

            y1 = self._alphas[last_alpha_containing]
            y2 = self._alphas[last_alpha_containing + 1]

            if (
                self.alpha_cuts[last_alpha_containing].min <= value
                and value <= self.alpha_cuts[last_alpha_containing + 1].min
            ):
                x1 = self.alpha_cuts[last_alpha_containing].min
                x2 = self.alpha_cuts[last_alpha_containing + 1].min

            else:
                x1 = self.alpha_cuts[last_alpha_containing].max
                x2 = self.alpha_cuts[last_alpha_containing + 1].max

            k = (y2 - y1) / (x2 - x1)
            q = y1 - (k * x1)

            return FuzzyMembership((k * Decimal(value)) + q)

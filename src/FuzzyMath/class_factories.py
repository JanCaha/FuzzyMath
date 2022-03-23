import re
from typing import List

from .class_fuzzy_number import FuzzyNumber
from .class_interval import Interval


class FuzzyNumberFactory:
    """
    Class that supports creation of fuzzy numbers based on different functions. All the functions are static.
    """

    @staticmethod
    def triangular(minimum: float,
                   kernel: float,
                   maximum: float,
                   number_of_cuts: int = None,
                   precision: int = None) -> FuzzyNumber:
        """
        Creates triangular `FuzzyNumber` based on input parameters.

        Parameters
        ----------
        minimum: float
            Minimal value of fuzzy number.

        kernel: float
            Kernel (midpoint) value of fuzzy number.

        maximum: float
            Maximal value of fuzzy number.

        number_of_cuts: int
            Number of alpha cuts.

        precision: int

        Returns
        -------
        FuzzyNumber
        """

        if not minimum <= kernel <= maximum:
            raise ValueError(
                "The fuzzy number is invalid. The structure needs to be `minimum` <= `kernel` "
                "<= `maximum`. Currently it is `{0}` <= `{1}` <= `{2}`, which does not hold.".
                format(minimum, kernel, maximum))

        if number_of_cuts is None or number_of_cuts <= 2:

            return FuzzyNumber(alphas=[0, 1],
                               alpha_cuts=[
                                   IntervalFactory.infimum_supremum(minimum,
                                                                    maximum,
                                                                    precision=precision),
                                   IntervalFactory.infimum_supremum(kernel,
                                                                    kernel,
                                                                    precision=precision)
            ],
                precision=precision)

        else:
            alphas = FuzzyNumber.get_alpha_cut_values(number_of_cuts, precision)

            intervals = [IntervalFactory.empty()] * len(alphas)

            i = 0
            for alpha in alphas:
                if alpha == 0:
                    intervals[i] = IntervalFactory.infimum_supremum(minimum,
                                                                    maximum,
                                                                    precision=precision)
                elif alpha == 1:
                    intervals[i] = IntervalFactory.infimum_supremum(kernel,
                                                                    kernel,
                                                                    precision=precision)
                else:
                    int_min = ((kernel - minimum) / (number_of_cuts - 1)) * i + minimum
                    int_max = maximum - ((maximum - kernel) / (number_of_cuts - 1)) * i
                    intervals[i] = IntervalFactory.infimum_supremum(int_min,
                                                                    int_max,
                                                                    precision=precision)
                i += 1

            return FuzzyNumber(alphas=alphas, alpha_cuts=intervals, precision=precision)

    @staticmethod
    def trapezoidal(minimum: float,
                    kernel_minimum: float,
                    kernel_maximum: float,
                    maximum: float,
                    number_of_cuts: int = None,
                    precision: int = None) -> FuzzyNumber:
        """
        Creates trapezoidal `FuzzyNumber` based on input parameters.

        Parameters
        ----------
        minimum: float
            Minimal value of fuzzy number.

        kernel_minimum: float
            Minimum kernel value of fuzzy number.

        kernel_maximum: float
            Maximal kernel value of fuzzy number.

        maximum: float
            Maximal value of fuzzy number.

        number_of_cuts: int
            Number of alpha cuts.

        precision: int

        Returns
        -------
        FuzzyNumber
        """

        if not minimum <= kernel_minimum <= kernel_maximum <= maximum:
            raise ValueError(
                "The fuzzy number is invalid. The structure needs to be "
                "`minimum` <= `kernel_minimum` <= `kernel_maximum` <= `maximum`. "
                "Currently it is `{0}` <= `{1}` <= `{2}` <= `{3}`, which does not hold.".format(
                    minimum, kernel_minimum, kernel_maximum, maximum))

        if number_of_cuts is None or number_of_cuts <= 2:

            return FuzzyNumber(alphas=[0, 1],
                               alpha_cuts=[
                                   IntervalFactory.infimum_supremum(minimum,
                                                                    maximum,
                                                                    precision=precision),
                                   IntervalFactory.infimum_supremum(kernel_minimum,
                                                                    kernel_maximum,
                                                                    precision=precision)
            ],
                precision=precision)

        else:
            alphas = FuzzyNumber.get_alpha_cut_values(number_of_cuts, precision)

            intervals = [IntervalFactory.empty()] * len(alphas)

            i = 0
            for alpha in alphas:
                if alpha == 0:
                    intervals[i] = IntervalFactory.infimum_supremum(minimum,
                                                                    maximum,
                                                                    precision=precision)
                elif alpha == 1:
                    intervals[i] = IntervalFactory.infimum_supremum(kernel_minimum,
                                                                    kernel_maximum,
                                                                    precision=precision)
                else:
                    int_min = ((kernel_minimum - minimum) / (number_of_cuts - 1)) * i + minimum
                    int_max = maximum - ((maximum - kernel_maximum) / (number_of_cuts - 1)) * i
                    intervals[i] = IntervalFactory.infimum_supremum(int_min,
                                                                    int_max,
                                                                    precision=precision)
                i += 1

            return FuzzyNumber(alphas=alphas, alpha_cuts=intervals, precision=precision)

    @staticmethod
    def crisp_number(value: float, precision: int = None) -> FuzzyNumber:
        """
        Creates `FuzzyNumber` based on input parameters.

        Parameters
        ----------
        value: float
            Value fuzzy number.

        precision: int

        Returns
        -------
        FuzzyNumber
        """

        return FuzzyNumber(alphas=[0, 1],
                           alpha_cuts=[
                               IntervalFactory.infimum_supremum(value, value, precision=precision),
                               IntervalFactory.infimum_supremum(value, value, precision=precision)
        ],
            precision=precision)

    @staticmethod
    def parse_string(string: str, precision: int = None) -> FuzzyNumber:
        """
        Creates `FuzzyNumber` based on input string. The input string should be output of `__repr__()` function of
        `FuzzyNumber`.

        Parameters
        ----------
        string: str

        precision: int

        Returns
        -------
        FuzzyNumber
        """

        re_a_cuts = re.compile(r"([0-9\.;,]+)")
        re_numbers = re.compile(r"[0-9\.]+")

        elements = re_a_cuts.findall(string)

        alphas: List[float] = [0] * len(elements)
        alpha_cuts: List[Interval] = [IntervalFactory.empty()] * len(elements)

        i: int = 0

        for a_cut_def in elements:

            numbers = re_numbers.findall(a_cut_def)

            if len(numbers) != 3:
                raise ValueError(
                    "Cannot parse FuzzyNumber from this definition. "
                    "Not all elements provide 3 values (alpha cut value and interval).")

            numbers = [float(x) for x in numbers]

            try:
                FuzzyNumber._validate_alpha(numbers[0])
            except ValueError as err:
                raise ValueError("`{}` element of Fuzzy Number is incorrectly defined. {}".format(
                    a_cut_def, err))

            alphas[i] = numbers[0]

            try:
                alpha_cuts[i] = IntervalFactory.infimum_supremum(numbers[1], numbers[2])
            except ValueError as err:
                raise ValueError("`{}` element of Fuzzy Number is incorrectly defined. {}".format(
                    a_cut_def, err))

            i += 1

        return FuzzyNumber(alphas, alpha_cuts, precision)


class IntervalFactory:
    """
    Class that supports creation of intervals based on different functions. All the functions are static.
    """

    @staticmethod
    def empty() -> Interval:
        """
        Creates empty interval, which has no values.

        Returns
        -------
        Interval
        """
        return Interval(float("nan"), float("nan"))

    @staticmethod
    def infimum_supremum(minimum: float, maximum: float, precision: int = None) -> Interval:
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
            raise ValueError(
                "The interval is invalid. `minimum` must be lower or equal to"
                " `maximum`. Currently it is `{0}` <= `{1}`, which does not hold.".format(
                    minimum, maximum))

        return Interval(minimum, maximum, precision=precision)

    @staticmethod
    def two_values(a: float, b: float, precision: int = None) -> Interval:
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
        return Interval(a, b, precision=precision)

    @staticmethod
    def midpoint_width(midpoint: float, width: float, precision: int = None) -> Interval:
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

        return Interval(a, b, precision=precision)

    @staticmethod
    def parse_string(string: str, precision: int = None) -> Interval:
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

        re_values = re.compile(r"\d+\.?\d*")

        numbers = re_values.findall(string)

        if len(numbers) != 2:
            raise ValueError("Cannot parse Interval from this definition. "
                             "Element does not provide 2 values (minimal and maximal).")

        return Interval(numbers[0], numbers[1], precision=precision)

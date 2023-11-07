import re
from abc import ABC
from decimal import Decimal, InvalidOperation
from typing import List, Optional, Union

from .class_fuzzy_number import FuzzyNumber
from .class_interval import Interval


class FactoryBase(ABC):
    @staticmethod
    def validate_variable(variable: Union[float, int, str, Decimal], variable_name: str) -> Decimal:
        """Checks that input variable can be converted to valid Decimal.

        Args:
            variable (Union[float, int, str, Decimal]): value to convert to Decimal.
            variable_name (str): name of variable for error message.

        Raises:
            InvalidOperation: if variable cannot be converted to Decimal.

        Returns:
            Decimal
        """
        try:
            var = Decimal(variable)
        except InvalidOperation as e:
            raise InvalidOperation(f"Cannot convert `{variable_name}` value ({variable}) to number.") from e
        return var

    @staticmethod
    def validate_alphas(alphas: List[Union[str, int, float, Decimal]], variable_name: str = "alphas") -> List[Decimal]:
        """Validate that all alphas are valid alpha values and converts them to Decimals.

        Args:
            alphas (List[Union[str, int, float, Decimal]]): List of alpha cut values.
            variable_name (str, optional): Name of variable for error message. Defaults to "alphas".

        Raises:
            InvalidOperation: If any alphas value cannot be converted to Decimal.

        Returns:
            List[Decimal]
        """
        decimal_alphas = []
        for alpha in alphas:
            try:
                decimal_alphas.append(Decimal(alpha))
            except InvalidOperation as e:
                raise InvalidOperation(f"Cannot convert `{variable_name}` value ({alpha}) to number.") from e
        return decimal_alphas


class FuzzyNumberFactory(FactoryBase):
    """
    Class that supports creation of fuzzy numbers based on different functions. All the functions are static.
    """

    @staticmethod
    def triangular(
        minimum: Union[str, int, float, Decimal],
        kernel: Union[str, int, float, Decimal],
        maximum: Union[str, int, float, Decimal],
        number_of_cuts: Optional[int] = None,
    ) -> FuzzyNumber:
        """
        Creates triangular `FuzzyNumber` based on input parameters.

        Parameters
        ----------
        minimum: Union[str, int, float, Decimal]
            Minimal value of fuzzy number.

        kernel: Union[str, int, float, Decimal]
            Kernel (midpoint) value of fuzzy number.

        maximum: Union[str, int, float, Decimal]
            Maximal value of fuzzy number.

        number_of_cuts: int
            Number of alpha cuts.

        Returns
        -------
        FuzzyNumber
        """

        minimum = FuzzyNumberFactory.validate_variable(minimum, "minimum")
        maximum = FuzzyNumberFactory.validate_variable(maximum, "maximum")
        kernel = FuzzyNumberFactory.validate_variable(kernel, "kernel")

        if not minimum <= kernel <= maximum:
            raise ValueError(
                "The fuzzy number is invalid. The structure needs to be `minimum` <= `kernel` "
                "<= `maximum`. Currently it is `{0}` <= `{1}` <= `{2}`, which does not hold.".format(
                    minimum, kernel, maximum
                )
            )

        if number_of_cuts is None or number_of_cuts <= 2:
            return FuzzyNumber(
                alphas=[Decimal(0), Decimal(1)],
                alpha_cuts=[
                    IntervalFactory.infimum_supremum(minimum, maximum),
                    IntervalFactory.infimum_supremum(kernel, kernel),
                ],
            )

        else:
            alphas = FuzzyNumber.get_alpha_cut_values(number_of_cuts)

            intervals = [IntervalFactory.empty()] * len(alphas)

            i = 0
            for alpha in alphas:
                if alpha == 0:
                    intervals[i] = IntervalFactory.infimum_supremum(minimum, maximum)
                elif alpha == 1:
                    intervals[i] = IntervalFactory.infimum_supremum(kernel, kernel)
                else:
                    int_min = ((kernel - minimum) / (number_of_cuts - 1)) * i + minimum
                    int_max = maximum - ((maximum - kernel) / (number_of_cuts - 1)) * i
                    intervals[i] = IntervalFactory.infimum_supremum(int_min, int_max)
                i += 1

            return FuzzyNumber(alphas=alphas, alpha_cuts=intervals)

    @staticmethod
    def trapezoidal(
        minimum: Union[str, int, float, Decimal],
        kernel_minimum: Union[str, int, float, Decimal],
        kernel_maximum: Union[str, int, float, Decimal],
        maximum: Union[str, int, float, Decimal],
        number_of_cuts: Optional[int] = None,
    ) -> FuzzyNumber:
        """
        Creates trapezoidal `FuzzyNumber` based on input parameters.

        Parameters
        ----------
        minimum: Union[str, int, float, Decimal]
            Minimal value of fuzzy number.

        kernel_minimum: Union[str, int, float, Decimal]
            Minimum kernel value of fuzzy number.

        kernel_maximum: Union[str, int, float, Decimal]
            Maximal kernel value of fuzzy number.

        maximum: Union[str, int, float, Decimal]
            Maximal value of fuzzy number.

        number_of_cuts: int
            Number of alpha cuts.

        Returns
        -------
        FuzzyNumber
        """

        minimum = FuzzyNumberFactory.validate_variable(minimum, "minimum")
        maximum = FuzzyNumberFactory.validate_variable(maximum, "maximum")
        kernel_minimum = FuzzyNumberFactory.validate_variable(kernel_minimum, "kernel_minimum")
        kernel_maximum = FuzzyNumberFactory.validate_variable(kernel_maximum, "kernel_maximum")

        if not minimum <= kernel_minimum <= kernel_maximum <= maximum:
            raise ValueError(
                "The fuzzy number is invalid. The structure needs to be "
                "`minimum` <= `kernel_minimum` <= `kernel_maximum` <= `maximum`. "
                "Currently it is `{0}` <= `{1}` <= `{2}` <= `{3}`, which does not hold.".format(
                    minimum, kernel_minimum, kernel_maximum, maximum
                )
            )

        if number_of_cuts is None or number_of_cuts <= 2:
            return FuzzyNumber(
                alphas=[Decimal(0), Decimal(1)],
                alpha_cuts=[
                    IntervalFactory.infimum_supremum(minimum, maximum),
                    IntervalFactory.infimum_supremum(kernel_minimum, kernel_maximum),
                ],
            )

        else:
            alphas = FuzzyNumber.get_alpha_cut_values(number_of_cuts)

            intervals = [IntervalFactory.empty()] * len(alphas)

            i = 0
            for alpha in alphas:
                if alpha == 0:
                    intervals[i] = IntervalFactory.infimum_supremum(minimum, maximum)
                elif alpha == 1:
                    intervals[i] = IntervalFactory.infimum_supremum(kernel_minimum, kernel_maximum)
                else:
                    int_min = ((kernel_minimum - minimum) / (number_of_cuts - 1)) * i + minimum
                    int_max = maximum - ((maximum - kernel_maximum) / (number_of_cuts - 1)) * i
                    intervals[i] = IntervalFactory.infimum_supremum(int_min, int_max)
                i += 1

            return FuzzyNumber(alphas=alphas, alpha_cuts=intervals)

    @staticmethod
    def crisp_number(value: Union[str, int, float, Decimal]) -> FuzzyNumber:
        """
        Creates `FuzzyNumber` based on input parameters.

        Parameters
        ----------
        value: Union[str, int, float, Decimal]
            Value fuzzy number.

        Returns
        -------
        FuzzyNumber
        """

        value = FuzzyNumberFactory.validate_variable(value, "value")

        return FuzzyNumber(
            alphas=[Decimal(0), Decimal(1)],
            alpha_cuts=[IntervalFactory.infimum_supremum(value, value), IntervalFactory.infimum_supremum(value, value)],
        )

    @staticmethod
    def parse_string(string: str) -> FuzzyNumber:
        """
        Creates `FuzzyNumber` based on input string. The input string should be output of `__repr__()` function of
        `FuzzyNumber`.

        Parameters
        ----------
        string: str

        Returns
        -------
        FuzzyNumber
        """

        re_a_cuts = re.compile(r"([0-9\.;,]+)")
        re_numbers = re.compile(r"[0-9\.]+")

        elements = re_a_cuts.findall(string)

        alphas: List[Decimal] = [Decimal(0)] * len(elements)
        alpha_cuts: List[Interval] = [IntervalFactory.empty()] * len(elements)

        i: int = 0

        for a_cut_def in elements:
            numbers = re_numbers.findall(a_cut_def)

            if len(numbers) != 3:
                raise ValueError(
                    "Cannot parse FuzzyNumber from this definition. "
                    "Not all elements provide 3 values (alpha cut value and interval)."
                )

            numbers = [Decimal(x) for x in numbers]

            try:
                FuzzyNumber._validate_alpha(numbers[0])  # pylint: disable=W0212
            except ValueError as err:
                raise ValueError("`{}` element of Fuzzy Number is incorrectly defined. {}".format(a_cut_def, err))

            alphas[i] = Decimal(numbers[0])

            try:
                alpha_cuts[i] = IntervalFactory.infimum_supremum(numbers[1], numbers[2])
            except ValueError as err:
                raise ValueError("`{}` element of Fuzzy Number is incorrectly defined. {}".format(a_cut_def, err))

            i += 1

        return FuzzyNumber(alphas, alpha_cuts)


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
        return Interval(Decimal("nan"), Decimal("nan"))

    @staticmethod
    def infimum_supremum(
        minimum: Union[str, int, float, Decimal], maximum: Union[str, int, float, Decimal]
    ) -> Interval:
        """
        Interval defined by minimum and maximum.

        Parameters
        ----------
        minimum: Union[str, int, float, Decimal]

        maximum: Union[str, int, float, Decimal]

        Returns
        -------
        Interval

        Raises
        -------
        ValueError
            If `minimum > maximum` which is not valid interval for this definition.
        """

        minimum = FuzzyNumberFactory.validate_variable(minimum, "minimum")
        maximum = FuzzyNumberFactory.validate_variable(maximum, "maximum")

        if minimum > maximum:
            raise ValueError(
                "The interval is invalid. `minimum` must be lower or equal to"
                " `maximum`. Currently it is `{0}` <= `{1}`, which does not hold.".format(minimum, maximum)
            )

        return Interval(minimum, maximum)

    @staticmethod
    def two_values(a: Union[str, int, float, Decimal], b: Union[str, int, float, Decimal]) -> Interval:
        """
        Interval defined by two values.

        Parameters
        ----------
        a: Union[str, int, float, Decimal]

        b: Union[str, int, float, Decimal]

        Returns
        -------
        Interval
        """
        return Interval(a, b)

    @staticmethod
    def midpoint_width(midpoint: Union[str, int, float, Decimal], width: Union[str, int, float, Decimal]) -> Interval:
        """
        Interval defined by midpoint and width. The interval is [midpoint - width, midpoint + width].

        Parameters
        ----------
        midpoint: Union[str, int, float, Decimal]

        width: Union[str, int, float, Decimal]

        Returns
        -------
        Interval

        Raises
        -------
        ArithmeticError
            If `width < 0` which is not valid width definition.
        """
        width = FuzzyNumberFactory.validate_variable(width, "width")
        midpoint = FuzzyNumberFactory.validate_variable(midpoint, "midpoint")

        if width < 0:
            raise ArithmeticError(
                "`width` of interval must number higher or at least equal to 0. "
                "The value `{0}` does not fulfill this.".format(width)
            )

        a = midpoint - (width / Decimal(2))
        b = midpoint + (width / Decimal(2))

        return Interval(a, b)

    @staticmethod
    def parse_string(string: str) -> Interval:
        """
        Creates `Interval` based on input string. The input string should be output of `__repr__()` function of
        `Interval`.

        Parameters
        ----------
        string: str

        Returns
        -------
        Interval
        """

        re_values = re.compile(r"\d+\.?\d*")

        numbers = re_values.findall(string)

        if len(numbers) != 2:
            raise ValueError(
                "Cannot parse Interval from this definition. "
                "Element does not provide 2 values (minimal and maximal)."
            )

        return Interval(numbers[0], numbers[1])

from typing import Union

from FuzzyMath.fuzzymath_utils import get_precision


class PossibilisticMembership:
    """
    Class that represents possibilistic membership in terms of possibility and necessity.
    ...
    Attributes
    ----------
    _possibility: float

    _necessity: float
    """

    __slots__ = ("_possibility", "_necessity")

    def __init__(self, possibility: Union[float, int], necessity: Union[float, int]) -> None:
        """
        Basic creator for the class.

        Parameters
        ----------
        possibility : Union[float, int]

        necessity : Union[float, int]

        Raises
        ------
        TypeError
            If either input variable is not `int` or `float`.
        ValueError
            If value of either variable is not from interval [0, 1]. Necessity must be smaller or equal to possibility.
        """

        self._possibility = 0.0
        self._necessity = 0.0

        if not isinstance(possibility, (int, float)):
            raise TypeError(
                f"Possibility value must be a `int` or `float`, it can not be `{type(possibility).__name__}`"
            )

        if not isinstance(necessity, (int, float)):
            raise TypeError(
                f"Necessity value must be a `int` or `float`, it can not be `{type(necessity).__name__}`"
            )

        if possibility < 0 or 1 < possibility:
            raise ValueError(
                f"Possibility value must be from range [0, 1], it is `{possibility}`.")

        if necessity < 0 or 1 < necessity:
            raise ValueError(f"Necessity value must be from range [0, 1], it is `{necessity}`.")

        if possibility < necessity:
            raise ValueError(
                f"Possibility value must be equal or larger then necessity. "
                f"Currently this does not hold for for values possibility values `{possibility}` and necessity `{necessity}`."
            )

        self._possibility = round(float(possibility), get_precision())
        self._necessity = round(float(necessity), get_precision())

    @property
    def possibility(self) -> float:
        """
        Property getter for the value.

        Returns
        -------
        float
        """

        return self._possibility

    @property
    def necessity(self) -> float:
        """
        Property getter for the value.

        Returns
        -------
        float
        """

        return self._necessity

    def __repr__(self) -> str:
        return "PossibilisticMembership(possibility: {0}, necessity: {1})".format(
            self._possibility, self._necessity)


class FuzzyMembership:
    """
    Class that represents fuzzy membership in terms of membership.
    ...
    Attributes
    ----------
    _membership: float
    """

    __slots__ = ("_membership")

    def __init__(self, membership: Union[float, int]) -> None:
        """
        Basic creator for the class.

        Parameters
        ----------
        membership : Union[float, int]

        Raises
        ------
        TypeError
            If either input variable is not `int` or `float`.
        ValueError
            If value of either variable is not from interval [0, 1].
        """

        self._membership = 0.0

        if not isinstance(membership, (int, float)):
            raise TypeError(
                f"Membership value must be a `int` or `float`, it can not be `{type(membership).__name__}`"
            )

        if membership < 0 or 1 < membership:
            raise ValueError(f"Membership value must be from range [0, 1], it is `{membership}`.")

        self._membership = round(float(membership), get_precision())

    @property
    def membership(self) -> float:
        """
        Property getter for the value.

        Returns
        -------
        float
        """

        return self._membership

    def __repr__(self) -> str:
        return "FuzzyMembership({0})".format(self._membership)

    def __eq__(self, __o: object) -> bool:

        if not isinstance(__o, (int, float, FuzzyMembership)):
            return NotImplemented

        if isinstance(__o, (int, float)):
            return self.membership == __o

        if isinstance(__o, FuzzyMembership):
            return self.membership == __o.membership

        # just for case, should not happen
        return False

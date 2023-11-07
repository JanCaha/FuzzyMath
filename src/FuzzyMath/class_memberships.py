from decimal import Decimal, InvalidOperation
from typing import Union


class PossibilisticMembership:
    """
    Class that represents possibilistic membership in terms of possibility and necessity.
    ...
    Attributes
    ----------
    _possibility: Decimal

    _necessity: Decimal
    """

    __slots__ = ("_possibility", "_necessity")

    def __init__(
        self, possibility: Union[str, int, float, Decimal], necessity: Union[str, int, float, Decimal]
    ) -> None:
        """
        Basic creator for the class.

        Parameters
        ----------
        possibility : Union[str, int, float, Decimal]

        necessity : Union[str, int, float, Decimal]

        Raises
        ------
        TypeError
            If either input variable is not `int`, `float`, `str` or `Decimal`.
        ValueError
            If value of either variable is not from interval [0, 1]. Necessity must be smaller or equal to possibility.
        """

        self._possibility = Decimal(0.0)
        self._necessity = Decimal(0.0)

        if not isinstance(possibility, (int, float, str, Decimal)):
            raise TypeError(
                f"Possibility value must be `int`, `float`, `str` or `Decimal`"
                f"it can not be `{type(possibility).__name__}`"
            )

        if not isinstance(necessity, (int, float, str, Decimal)):
            raise TypeError(
                f"Necessity value must be `int`, `float`, `str` or `Decimal`"
                f"it can not be `{type(necessity).__name__}`"
            )

        self._possibility = self._possibility.normalize()
        self._necessity = self._necessity.normalize()

        try:
            self._possibility = Decimal(possibility)
        except InvalidOperation as e:
            raise InvalidOperation(f"Cannot convert `possibility` value ({possibility}) to number.") from e

        try:
            self._necessity = Decimal(necessity)
        except InvalidOperation as e:
            raise InvalidOperation(f"Cannot convert `necessity` value ({necessity}) to number.") from e

        if self._possibility < 0 or 1 < self._possibility:
            raise ValueError(f"Possibility value must be from range [0, 1], it is `{possibility}`.")

        if self._necessity < 0 or 1 < self._necessity:
            raise ValueError(f"Necessity value must be from range [0, 1], it is `{necessity}`.")

        if self._possibility < self._necessity:
            raise ValueError(
                f"Possibility value must be equal or larger then necessity. "
                f"Currently this does not hold for for values possibility values "
                f"`{possibility}` and necessity `{necessity}`."
            )

    @property
    def possibility(self) -> Decimal:
        """
        Property getter for the value.

        Returns
        -------
        Decimal
        """

        return self._possibility

    @property
    def necessity(self) -> Decimal:
        """
        Property getter for the value.

        Returns
        -------
        Decimal
        """

        return self._necessity

    def __repr__(self) -> str:
        return "PossibilisticMembership(possibility: {self._possibility}, necessity: {self._necessity})"

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, PossibilisticMembership):
            return NotImplemented

        else:
            return self.possibility == __o.possibility and self.necessity == __o.necessity


class FuzzyMembership:
    """
    Class that represents fuzzy membership in terms of membership.
    ...
    Attributes
    ----------
    _membership: Decimal
    """

    __slots__ = ["_membership"]

    def __init__(self, membership: Union[str, int, float, Decimal]) -> None:
        """
        Basic creator for the class.

        Parameters
        ----------
        membership : Union[str, int, float, Decimal]

        Raises
        ------
        TypeError
            If either input variable is not `int`, `float`, `str` or `Decimal`.
        ValueError
            If value of either variable is not from interval [0, 1].
        """

        self._membership = Decimal(0)

        if not isinstance(membership, (int, float, str, Decimal)):
            raise TypeError(
                f"Membership value must be a `int`, `float`, `str` or `Decimal`"
                f" it can not be `{type(membership).__name__}`"
            )

        try:
            self._membership = Decimal(membership)
        except InvalidOperation as e:
            raise InvalidOperation(f"Cannot convert `membership` value ({membership}) to number.") from e

        self._membership = self._membership.normalize()

        if self._membership < 0 or 1 < self._membership:
            raise ValueError(f"Membership value must be from range [0, 1], it is `{membership}`.")

    @property
    def membership(self) -> Decimal:
        """
        Property getter for the value.

        Returns
        -------
        Decimal
        """

        return self._membership

    def __repr__(self) -> str:
        return f"FuzzyMembership({self._membership})"

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, (int, float, FuzzyMembership, Decimal)):
            return NotImplemented

        if isinstance(__o, Decimal):
            return self.membership == __o

        if isinstance(__o, (int, float)):
            return self.membership == Decimal(__o)

        if isinstance(__o, FuzzyMembership):
            return self.membership == __o.membership

        # just for case, should not happen
        return False

from typing import Union


class PossibilisticMembership:

    __slots__ = ("_possibility", "_necessity")

    def __init__(self, poss: float, nec: float) -> None:

        if poss < 0 or 1 < poss:
            raise ValueError(f"Possibility value must be from range [0, 1], it is `{poss}`.")

        if nec < 0 or 1 < nec:
            raise ValueError(f"Necessity value must be from range [0, 1], it is `{nec}`.")

        if poss < nec:
            raise ValueError(
                f"Possibility value must be equal or larger then necessity. "
                f"Currently this does not hold for for values possibility values `{poss}` and necessity `{nec}`.")

        self._possibility = poss
        self._necessity = nec

    @property
    def possibility(self) -> float:
        return self._possibility

    @property
    def necessity(self) -> float:
        return self._necessity

    def __repr__(self) -> str:
        return "PossibilisticMembership(possibility: {0}, necessity: {1})".format(self._possibility, self._necessity)


class FuzzyMembership:

    __slots__ = ("_membership")

    def __init__(self, membership: Union[float, int]) -> None:

        self._membership = 0.0

        if not isinstance(membership, (int, float)):
            raise TypeError(
                f"Membership value must be a `int` or `float`, it can not be `{type(membership).__name__}`")

        if membership < 0 or 1 < membership:
            raise ValueError(f"Membership value must be from range [0, 1], it is `{membership}`.")

        self._membership = membership

    @property
    def membership(self) -> float:
        return self._membership

    def __repr__(self) -> str:
        return "FuzzyMembership({0})".format(self._membership)

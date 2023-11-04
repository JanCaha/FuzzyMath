import inspect
from typing import Literal, Tuple

from .class_memberships import FuzzyMembership, PossibilisticMembership

fuzzyAnds = Literal["min", "product", "drastic", "Lukasiewicz", "Nilpotent", "Hamacher"]
fuzzyOrs = Literal["max", "product", "drastic", "Lukasiewicz", "Nilpotent", "Hamacher"]

FUZZY_AND_NAMES = ["min", "product", "drastic", "Lukasiewicz", "Nilpotent", "Hamacher"]
FUZZY_OR_NAMES = ["max", "product", "drastic", "Lukasiewicz", "Nilpotent", "Hamacher"]


class PossibilisticOperation:
    @staticmethod
    def _possibilities(
        a: PossibilisticMembership, b: PossibilisticMembership
    ) -> Tuple[FuzzyMembership, FuzzyMembership]:
        return (FuzzyMembership(a.possibility), FuzzyMembership(b.possibility))

    @staticmethod
    def _necessities(a: PossibilisticMembership, b: PossibilisticMembership) -> Tuple[FuzzyMembership, FuzzyMembership]:
        return (FuzzyMembership(a.necessity), FuzzyMembership(b.necessity))


class FuzzyAnd:
    @staticmethod
    def min(a: FuzzyMembership, b: FuzzyMembership) -> FuzzyMembership:
        return FuzzyMembership(min(a.membership, b.membership))

    @staticmethod
    def product(a: FuzzyMembership, b: FuzzyMembership) -> FuzzyMembership:
        return FuzzyMembership(a.membership * b.membership)

    @staticmethod
    def drastic(a: FuzzyMembership, b: FuzzyMembership) -> FuzzyMembership:
        if a.membership == 1:
            return b
        elif b.membership == 1:
            return a
        else:
            return FuzzyMembership(0)

    @staticmethod
    def Lukasiewicz(a: FuzzyMembership, b: FuzzyMembership) -> FuzzyMembership:
        return FuzzyMembership(max(0, a.membership + b.membership - 1))

    @staticmethod
    def Nilpotent(a: FuzzyMembership, b: FuzzyMembership) -> FuzzyMembership:
        if (a.membership + b.membership) > 1:
            return FuzzyMembership(min(a.membership, b.membership))
        else:
            return FuzzyMembership(0)

    @staticmethod
    def Hamacher(a: FuzzyMembership, b: FuzzyMembership) -> FuzzyMembership:
        if a.membership == 0 and b.membership == 0:
            return FuzzyMembership(0)
        else:
            return FuzzyMembership(
                (a.membership * b.membership) / (a.membership + b.membership - (a.membership * b.membership))
            )

    @staticmethod
    def fuzzyAnd(a: FuzzyMembership, b: FuzzyMembership, type: fuzzyAnds):
        if type not in FUZZY_AND_NAMES:
            raise ValueError(
                "Unknown value `{}` for `fuzzy and`. Known types are `{}`.".format(type, ", ".join(FUZZY_AND_NAMES))
            )

        method_to_call = getattr(FuzzyAnd, type)
        return method_to_call(a, b)


class PossibilisticAnd(PossibilisticOperation):
    @staticmethod
    def min(a: PossibilisticMembership, b: PossibilisticMembership):
        type = inspect.currentframe().f_code.co_name

        return PossibilisticAnd.possibilisticAnd(a, b, type)

    @staticmethod
    def product(a: PossibilisticMembership, b: PossibilisticMembership):
        type = inspect.currentframe().f_code.co_name

        return PossibilisticAnd.possibilisticAnd(a, b, type)

    @staticmethod
    def drastic(a: PossibilisticMembership, b: PossibilisticMembership):
        type = inspect.currentframe().f_code.co_name

        return PossibilisticAnd.possibilisticAnd(a, b, type)

    @staticmethod
    def Lukasiewicz(a: PossibilisticMembership, b: PossibilisticMembership):
        type = inspect.currentframe().f_code.co_name

        return PossibilisticAnd.possibilisticAnd(a, b, type)

    @staticmethod
    def Nilpotent(a: PossibilisticMembership, b: PossibilisticMembership):
        type = inspect.currentframe().f_code.co_name

        return PossibilisticAnd.possibilisticAnd(a, b, type)

    @staticmethod
    def Hamacher(a: PossibilisticMembership, b: PossibilisticMembership):
        type = inspect.currentframe().f_code.co_name

        return PossibilisticAnd.possibilisticAnd(a, b, type)

    @staticmethod
    def possibilisticAnd(a: PossibilisticMembership, b: PossibilisticMembership, type: fuzzyAnds):
        if type not in FUZZY_AND_NAMES:
            raise ValueError(
                "Unknown value `{}` for `possibilistic and`. Known types are `{}`.".format(
                    type, ", ".join(FUZZY_AND_NAMES)
                )
            )

        method_to_call = getattr(FuzzyAnd, type)

        a_poss, b_poss = PossibilisticAnd._possibilities(a, b)

        a_nec, b_nec = PossibilisticAnd._necessities(a, b)

        return PossibilisticMembership(
            method_to_call(a_poss, b_poss).membership, method_to_call(a_nec, b_nec).membership
        )


class FuzzyOr:
    @staticmethod
    def max(a: FuzzyMembership, b: FuzzyMembership) -> FuzzyMembership:
        return FuzzyMembership(max(a.membership, b.membership))

    @staticmethod
    def product(a: FuzzyMembership, b: FuzzyMembership) -> FuzzyMembership:
        return FuzzyMembership(a.membership + b.membership - (a.membership * b.membership))

    @staticmethod
    def drastic(a: FuzzyMembership, b: FuzzyMembership) -> FuzzyMembership:
        if a.membership == 0:
            return b
        elif b.membership == 0:
            return a
        else:
            return FuzzyMembership(0)

    @staticmethod
    def Lukasiewicz(a: FuzzyMembership, b: FuzzyMembership) -> FuzzyMembership:
        return FuzzyMembership(min(1, a.membership + b.membership))

    @staticmethod
    def Nilpotent(a: FuzzyMembership, b: FuzzyMembership) -> FuzzyMembership:
        if (a.membership + b.membership) < 1:
            return FuzzyMembership(max(a.membership, b.membership))
        else:
            return FuzzyMembership(1)

    @staticmethod
    def Hamacher(a: FuzzyMembership, b: FuzzyMembership) -> FuzzyMembership:
        return FuzzyMembership((a.membership + b.membership) / (1 + (a.membership * b.membership)))

    @staticmethod
    def fuzzyOr(a: FuzzyMembership, b: FuzzyMembership, type: fuzzyOrs):
        if type not in FUZZY_OR_NAMES:
            raise ValueError(
                "Unknown value `{}` for `fuzzy or`. Known types are `{}`.".format(type, ", ".join(FUZZY_OR_NAMES))
            )

        method_to_call = getattr(FuzzyOr, type)
        return method_to_call(a, b)


class PossibilisticOr(PossibilisticOperation):
    @staticmethod
    def max(a: PossibilisticMembership, b: PossibilisticMembership):
        type = inspect.currentframe().f_code.co_name

        return PossibilisticOr.possibilisticOr(a, b, type)

    @staticmethod
    def product(a: PossibilisticMembership, b: PossibilisticMembership):
        type = inspect.currentframe().f_code.co_name

        return PossibilisticOr.possibilisticOr(a, b, type)

    @staticmethod
    def drastic(a: PossibilisticMembership, b: PossibilisticMembership):
        type = inspect.currentframe().f_code.co_name

        return PossibilisticOr.possibilisticOr(a, b, type)

    @staticmethod
    def Lukasiewicz(a: PossibilisticMembership, b: PossibilisticMembership):
        type = inspect.currentframe().f_code.co_name

        return PossibilisticOr.possibilisticOr(a, b, type)

    @staticmethod
    def Nilpotent(a: PossibilisticMembership, b: PossibilisticMembership):
        type = inspect.currentframe().f_code.co_name

        return PossibilisticOr.possibilisticOr(a, b, type)

    @staticmethod
    def Hamacher(a: PossibilisticMembership, b: PossibilisticMembership):
        type = inspect.currentframe().f_code.co_name

        return PossibilisticOr.possibilisticOr(a, b, type)

    @staticmethod
    def possibilisticOr(a: PossibilisticMembership, b: PossibilisticMembership, type: fuzzyOrs):
        if type not in FUZZY_OR_NAMES:
            raise ValueError(
                "Unknown value `{}` for `possibilistic or`. Known types are `{}`.".format(
                    type, ", ".join(FUZZY_OR_NAMES)
                )
            )

        method_to_call = getattr(FuzzyOr, type)

        a_poss, b_poss = PossibilisticOr._possibilities(a, b)

        a_nec, b_nec = PossibilisticOr._necessities(a, b)

        return PossibilisticMembership(
            method_to_call(a_poss, b_poss).membership, method_to_call(a_nec, b_nec).membership
        )

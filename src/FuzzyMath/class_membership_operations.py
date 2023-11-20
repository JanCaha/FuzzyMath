from decimal import Decimal
from typing import Literal, Tuple

from .class_memberships import FuzzyMembership, PossibilisticMembership

fuzzy_and_names = Literal["min", "product", "drastic", "Lukasiewicz", "Nilpotent", "Hamacher"]  # pylint: disable=C0103
fuzzy_or_names = Literal["max", "product", "drastic", "Lukasiewicz", "Nilpotent", "Hamacher"]  # pylint: disable=C0103

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
    def Lukasiewicz(a: FuzzyMembership, b: FuzzyMembership) -> FuzzyMembership:  # pylint: disable=C0103
        return FuzzyMembership(max(Decimal(0), a.membership + b.membership - Decimal(1)))

    @staticmethod
    def Nilpotent(a: FuzzyMembership, b: FuzzyMembership) -> FuzzyMembership:  # pylint: disable=C0103
        if (a.membership + b.membership) > 1:
            return FuzzyMembership(min(a.membership, b.membership))
        else:
            return FuzzyMembership(0)

    @staticmethod
    def Hamacher(a: FuzzyMembership, b: FuzzyMembership) -> FuzzyMembership:  # pylint: disable=C0103
        if a.membership == 0 and b.membership == 0:
            return FuzzyMembership(0)
        else:
            return FuzzyMembership(
                (a.membership * b.membership) / (a.membership + b.membership - (a.membership * b.membership))
            )

    @staticmethod
    def fuzzy_and(a: FuzzyMembership, b: FuzzyMembership, and_type: fuzzy_and_names):
        if and_type not in FUZZY_AND_NAMES:
            raise ValueError(
                f"Unknown value `{and_type}` for `fuzzy and`. Known types are `{', '.join(FUZZY_AND_NAMES)}`."
            )

        method_to_call = getattr(FuzzyAnd, and_type)
        return method_to_call(a, b)


class PossibilisticAnd(PossibilisticOperation):
    @staticmethod
    def min(a: PossibilisticMembership, b: PossibilisticMembership):
        return PossibilisticAnd.possibilistic_and(a, b, "min")

    @staticmethod
    def product(a: PossibilisticMembership, b: PossibilisticMembership):
        return PossibilisticAnd.possibilistic_and(a, b, "product")

    @staticmethod
    def drastic(a: PossibilisticMembership, b: PossibilisticMembership):
        return PossibilisticAnd.possibilistic_and(a, b, "drastic")

    @staticmethod
    def Lukasiewicz(a: PossibilisticMembership, b: PossibilisticMembership):  # pylint: disable=C0103
        return PossibilisticAnd.possibilistic_and(a, b, "Lukasiewicz")

    @staticmethod
    def Nilpotent(a: PossibilisticMembership, b: PossibilisticMembership):  # pylint: disable=C0103
        return PossibilisticAnd.possibilistic_and(a, b, "Nilpotent")

    @staticmethod
    def Hamacher(a: PossibilisticMembership, b: PossibilisticMembership):  # pylint: disable=C0103
        return PossibilisticAnd.possibilistic_and(a, b, "Hamacher")

    @staticmethod
    def possibilistic_and(a: PossibilisticMembership, b: PossibilisticMembership, and_type: fuzzy_and_names):
        if and_type not in FUZZY_AND_NAMES:
            raise ValueError(
                f"Unknown value `{and_type}` for `possibilistic and`. Known types are `{', '.join(FUZZY_OR_NAMES)}`."
            )

        method_to_call = getattr(FuzzyAnd, and_type)

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
    def Lukasiewicz(a: FuzzyMembership, b: FuzzyMembership) -> FuzzyMembership:  # pylint: disable=C0103
        return FuzzyMembership(min(Decimal(1), a.membership + b.membership))

    @staticmethod
    def Nilpotent(a: FuzzyMembership, b: FuzzyMembership) -> FuzzyMembership:  # pylint: disable=C0103
        if (a.membership + b.membership) < 1:
            return FuzzyMembership(max(a.membership, b.membership))
        else:
            return FuzzyMembership(1)

    @staticmethod
    def Hamacher(a: FuzzyMembership, b: FuzzyMembership) -> FuzzyMembership:  # pylint: disable=C0103
        return FuzzyMembership((a.membership + b.membership) / (1 + (a.membership * b.membership)))

    @staticmethod
    def fuzzy_or(a: FuzzyMembership, b: FuzzyMembership, or_type: fuzzy_or_names):
        if or_type not in FUZZY_OR_NAMES:
            raise ValueError(
                f"Unknown value `{or_type}` for `fuzzy or`. Known types are `{', '.join(FUZZY_OR_NAMES)}`."
            )

        method_to_call = getattr(FuzzyOr, or_type)
        return method_to_call(a, b)


class PossibilisticOr(PossibilisticOperation):
    @staticmethod
    def max(a: PossibilisticMembership, b: PossibilisticMembership):
        return PossibilisticOr.possibilistic_or(a, b, "max")

    @staticmethod
    def product(a: PossibilisticMembership, b: PossibilisticMembership):
        return PossibilisticOr.possibilistic_or(a, b, "product")

    @staticmethod
    def drastic(a: PossibilisticMembership, b: PossibilisticMembership):
        return PossibilisticOr.possibilistic_or(a, b, "drastic")

    @staticmethod
    def Lukasiewicz(a: PossibilisticMembership, b: PossibilisticMembership):  # pylint: disable=C0103
        return PossibilisticOr.possibilistic_or(a, b, "Lukasiewicz")

    @staticmethod
    def Nilpotent(a: PossibilisticMembership, b: PossibilisticMembership):  # pylint: disable=C0103
        return PossibilisticOr.possibilistic_or(a, b, "Nilpotent")

    @staticmethod
    def Hamacher(a: PossibilisticMembership, b: PossibilisticMembership):  # pylint: disable=C0103
        return PossibilisticOr.possibilistic_or(a, b, "Hamacher")

    @staticmethod
    def possibilistic_or(a: PossibilisticMembership, b: PossibilisticMembership, or_type: fuzzy_or_names):
        if or_type not in FUZZY_OR_NAMES:
            raise ValueError(
                f"Unknown value `{or_type}` for `possibilistic or`. Known types are `{', '.join(FUZZY_OR_NAMES)}`."
            )

        method_to_call = getattr(FuzzyOr, or_type)

        a_poss, b_poss = PossibilisticOr._possibilities(a, b)

        a_nec, b_nec = PossibilisticOr._necessities(a, b)

        return PossibilisticMembership(
            method_to_call(a_poss, b_poss).membership, method_to_call(a_nec, b_nec).membership
        )

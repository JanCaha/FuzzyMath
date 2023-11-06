# flake8: noqa: F401
"""
Python package `FuzzyMath` is a small lightweight library for Python (version >= 3.7) that performs basic
Interval and Fuzzy Arithmetic.
"""

from .class_factories import FuzzyNumberFactory, IntervalFactory
from .class_fuzzy_number import FuzzyNumber
from .class_interval import Interval
from .class_membership_operations import FuzzyAnd, FuzzyOr, PossibilisticAnd, PossibilisticOr
from .class_memberships import FuzzyMembership, PossibilisticMembership
from .class_precision import FuzzyMathPrecision, FuzzyMathPrecisionContext
from .fuzzynumber_comparisons import (
    exceedance,
    necessity_exceedance,
    necessity_strict_exceedance,
    necessity_strict_undervaluation,
    necessity_undervaluation,
    possibility_exceedance,
    possibility_strict_exceedance,
    possibility_strict_undervaluation,
    possibility_undervaluation,
    strict_exceedance,
    strict_undervaluation,
    undervaluation,
)

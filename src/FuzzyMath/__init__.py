# flake8: noqa: F401
"""
Python package `FuzzyMath` is a small lightweight library for Python (version >= 3.7) that performs basic
Interval and Fuzzy Arithmetic.
"""

from .class_interval import Interval
from .class_fuzzy_number import FuzzyNumber
from .class_factories import FuzzyNumberFactory, IntervalFactory
from .class_memberships import PossibilisticMembership, FuzzyMembership

from .fuzzynumber_comparisons import (possibility_exceedance,
                                      possibility_strict_exceedance,
                                      necessity_exceedance,
                                      necessity_strict_exceedance,
                                      possibility_undervaluation,
                                      necessity_undervaluation,
                                      possibility_strict_undervaluation,
                                      necessity_strict_undervaluation,
                                      exceedance,
                                      strict_exceedance,
                                      undervaluation,
                                      strict_undervaluation)

from .fuzzymath_utils import set_precision, get_precision

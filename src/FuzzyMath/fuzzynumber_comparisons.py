from typing import List

from .class_fuzzy_number import FuzzyNumber
from .class_memberships import PossibilisticMembership


def possibility_exceedance(fn_a: FuzzyNumber, fn_b: FuzzyNumber) -> float:

    if fn_a.max <= fn_b.min:
        return 0

    elif fn_a.kernel_min >= fn_b.kernel_min:
        return 1

    else:

        alphas = FuzzyNumber._prepare_alphas(fn_a.alpha_levels,
                                             fn_b.alpha_levels)

        fn_a_values = fn_a.get_alpha_cuts_maxs(alphas, order_by_alphas_from_one=True)
        fn_b_values = fn_b.get_alpha_cuts_mins(alphas, order_by_alphas_from_one=True)

        index = 0
        for i in range(len(alphas)):

            if fn_a_values[i] >= fn_b_values[i]:
                break

            index += 1

        alphas.reverse()

        return __value_intersection_y(fn_a_values, fn_b_values, alphas,
                                      index=index, index_change=-1)


def necessity_exceedance(fn_a: FuzzyNumber, fn_b: FuzzyNumber) -> float:

    if fn_a.kernel_min <= fn_b.min:
        return 0

    elif fn_a.min >= fn_b.kernel_min:
        return 1

    else:

        alphas = FuzzyNumber._prepare_alphas(fn_a.alpha_levels,
                                             fn_b.alpha_levels)

        fn_a_values = fn_a.get_alpha_cuts_mins(alphas, order_by_alphas_from_one=True)
        fn_b_values = fn_b.get_alpha_cuts_mins(alphas)

        index = 0
        for i in range(len(alphas)):

            if fn_a_values[i] >= fn_b_values[i]:
                break

            index += 1

        return __value_intersection_y(fn_a_values, fn_b_values, alphas,
                                      index=index, index_change=-1)


def possibility_strict_exceedance(fn_a: FuzzyNumber, fn_b: FuzzyNumber) -> float:

    if fn_a.max < fn_b.max:
        return 0

    elif fn_a.kernel_min > fn_b.max:
        return 1

    else:

        alphas = FuzzyNumber._prepare_alphas(fn_a.alpha_levels,
                                             fn_b.alpha_levels)

        fn_a_values = fn_a.get_alpha_cuts_maxs(alphas)
        fn_b_values = fn_b.get_alpha_cuts_maxs(alphas, order_by_alphas_from_one=True)

        index = 0
        for i in range(len(alphas)):

            if fn_a_values[i] >= fn_b_values[i]:
                break

            index += 1

        return __value_intersection_y(fn_a_values, fn_b_values, alphas,
                                      index=index, index_change=1)


def necessity_strict_exceedance(fn_a: FuzzyNumber, fn_b: FuzzyNumber) -> float:

    if fn_a.kernel_min < fn_b.kernel_max:
        return 0

    elif fn_a.min > fn_b.max:
        return 1

    else:

        alphas = FuzzyNumber._prepare_alphas(fn_a.alpha_levels,
                                             fn_b.alpha_levels)

        fn_a_values = fn_a.get_alpha_cuts_mins(alphas, order_by_alphas_from_one=True)
        fn_b_values = fn_b.get_alpha_cuts_maxs(alphas, order_by_alphas_from_one=True)

        index = 0
        for i in range(len(alphas)):

            if fn_a_values[i] >= fn_b_values[i]:
                break

            index += 1

        return __value_intersection_y(fn_a_values, fn_b_values, alphas,
                                      index=index, index_change=1)


def possibility_undervaluation(fn_a: FuzzyNumber, fn_b: FuzzyNumber) -> float:
    return 1 - necessity_strict_exceedance(fn_a, fn_b)


def necessity_undervaluation(fn_a: FuzzyNumber, fn_b: FuzzyNumber) -> float:
    return 1 - possibility_strict_exceedance(fn_a, fn_b)


def possibility_strict_undervaluation(fn_a: FuzzyNumber, fn_b: FuzzyNumber) -> float:
    return 1 - necessity_exceedance(fn_a, fn_b)


def necessity_strict_undervaluation(fn_a: FuzzyNumber, fn_b: FuzzyNumber) -> float:
    return 1 - possibility_exceedance(fn_a, fn_b)


def __value_intersection_y(fn_a_values: List[float],
                           fn_b_values: List[float],
                           alphas: List[float],
                           index: int,
                           index_change: int):

    return __intersection_y(fn_a_values[index], alphas[index],
                            fn_a_values[index + index_change], alphas[index + index_change],
                            fn_b_values[index], alphas[index],
                            fn_b_values[index + index_change], alphas[index + index_change])


def __intersection_y(x1, y1,
                     x2, y2,
                     x3, y3,
                     x4, y4):
    x12 = x1 - x2
    x34 = x3 - x4
    y12 = y1 - y2
    y34 = y3 - y4

    c = x12 * y34 - y12 * x34

    a = x1 * y2 - y1 * x2
    b = x3 * y4 - y3 * x4

    # x = (a * x34 - b * x12) / c
    y = (a * y34 - b * y12) / c

    return y


def exceedance(fn_a: FuzzyNumber, fn_b: FuzzyNumber) -> PossibilisticMembership:

    return PossibilisticMembership(possibility_exceedance(fn_a, fn_b),
                                   necessity_exceedance(fn_a, fn_b))


def strict_exceedance(fn_a: FuzzyNumber, fn_b: FuzzyNumber) -> PossibilisticMembership:

    return PossibilisticMembership(possibility_strict_exceedance(fn_a, fn_b),
                                   necessity_strict_exceedance(fn_a, fn_b))


def undervaluation(fn_a: FuzzyNumber, fn_b: FuzzyNumber) -> PossibilisticMembership:

    return PossibilisticMembership(possibility_undervaluation(fn_a, fn_b),
                                   necessity_undervaluation(fn_a, fn_b))


def strict_undervaluation(fn_a: FuzzyNumber, fn_b: FuzzyNumber) -> PossibilisticMembership:

    return PossibilisticMembership(possibility_strict_undervaluation(fn_a, fn_b),
                                   necessity_strict_undervaluation(fn_a, fn_b))

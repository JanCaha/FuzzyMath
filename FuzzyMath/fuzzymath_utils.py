import warnings
from typing import NoReturn

from . import config


def set_up_precision(precision: (float, int) = None, default_precision: int = 15) -> int:
    if precision is None:
        precision = default_precision
    if not isinstance(precision, (int, float)):
        warnings.warn("`precision` is not either `int` or `float`. "
                      "Using default value of precision `{0}`."
                      .format(default_precision), UserWarning)
        precision = default_precision
    if precision < 1 or precision > 15:
        raise ValueError("`precision` should be value from range `0` to `15`. It is `{0}`."
                         .format(precision))
    if precision != round(precision, 0):
        warnings.warn("`precision` should be number without decimal part. Retyping to Integer.")

    return int(precision)


def set_precision(precision: (float, int)) -> NoReturn:
    precision = set_up_precision(precision)

    config.precision = int(precision)


def get_precision() -> int:
    return config.precision

import pytest

from decimal import InvalidOperation

from FuzzyMath import FuzzyMembership, PossibilisticMembership


def test_fuzzy_membership():

    with pytest.raises(TypeError,
                       match="Membership value must be"):
        FuzzyMembership(FuzzyMembership(0))

    with pytest.raises(InvalidOperation,
                       match="Cannot convert"):
        FuzzyMembership("a")
    
    with pytest.raises(ValueError,
                       match="Membership value must be from range"):
        FuzzyMembership(-1)

    with pytest.raises(ValueError,
                       match="Membership value must be from range"):
        FuzzyMembership(2)

    fuzzy_membership = FuzzyMembership(0.5)

    assert str(fuzzy_membership) == "FuzzyMembership(0.5)"

    assert fuzzy_membership.membership == 0.5
    assert fuzzy_membership == 0.5
    assert fuzzy_membership == FuzzyMembership(0.5)
    
    fuzzy_membership = FuzzyMembership("0.5")

    assert str(fuzzy_membership) == "FuzzyMembership(0.5)"


def test_possibilistic_membership():

    with pytest.raises(InvalidOperation,
                       match="Cannot convert `possibility`"):
        PossibilisticMembership("a", 0.5)

    with pytest.raises(InvalidOperation,
                       match="Cannot convert `necessity`"):
        PossibilisticMembership(0.5, "a")

    with pytest.raises(TypeError,
                       match="Possibility value must be"):
        PossibilisticMembership(FuzzyMembership(0), 0.5)

    with pytest.raises(TypeError,
                       match="Necessity value must be"):
        PossibilisticMembership(0.5, FuzzyMembership(0))

    with pytest.raises(ValueError,
                       match="Possibility value must be from range"):
        PossibilisticMembership(1.5, 0.6)

    with pytest.raises(ValueError,
                       match="Necessity value must be from range"):
        PossibilisticMembership(0.5, -0.6)

    with pytest.raises(ValueError,
                       match="Possibility value must be equal or larger then necessity"):
        PossibilisticMembership(0.5, 0.6)

    possibilistic_membership = PossibilisticMembership(1.0, 0.5)

    assert str(possibilistic_membership) == "PossibilisticMembership(possibility: 1, necessity: 0.5)"

    assert possibilistic_membership.possibility == 1
    assert possibilistic_membership.necessity == 0.5

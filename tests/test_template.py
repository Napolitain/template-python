from hypothesis import given
from hypothesis import strategies as st

from template import add


def test_add() -> None:
    assert add(2, 3) == 5


# Property-based tests: hypothesis generates inputs and shrinks failures to a minimal case.
@given(st.integers(), st.integers())
def test_add_is_commutative(a: int, b: int) -> None:
    assert add(a, b) == add(b, a)


@given(st.integers())
def test_add_zero_is_identity(a: int) -> None:
    assert add(a, 0) == a

import pytest

from collatz_bench import core

needs_c = pytest.mark.skipif(core.backend() != "c", reason="lib C nao compilada")


def test_known_steps():
    assert core.steps_py(1) == 0
    assert core.steps_py(6) == 8
    assert core.steps_py(27) == 111


def test_longest_below_1000():
    assert core.longest_py(1000) == (871, 178)


def test_invalid_input():
    with pytest.raises(ValueError):
        core.steps_py(0)


@needs_c
def test_c_matches_python():
    for n in (1, 2, 3, 27, 97, 871, 6171):
        assert core.steps_c(n) == core.steps_py(n)
    assert core.longest_c(5000) == core.longest_py(5000)

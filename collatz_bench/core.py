"""Nucleo: implementacao em Python puro + ponte (ctypes) para a lib em C."""
import ctypes
import sys
from pathlib import Path
from typing import Optional, Tuple

_EXT = {"win32": ".dll", "darwin": ".dylib"}.get(sys.platform, ".so")
_LIB_PATH = Path(__file__).parent / "_native" / f"libcollatz{_EXT}"
_OVERFLOW = 2**64 - 1


def _load() -> Optional[ctypes.CDLL]:
    try:
        lib = ctypes.CDLL(str(_LIB_PATH))
    except OSError:
        return None
    u64 = ctypes.c_uint64
    lib.collatz_steps.argtypes = [u64]
    lib.collatz_steps.restype = u64
    lib.collatz_longest.argtypes = [u64, ctypes.POINTER(u64), ctypes.POINTER(u64)]
    lib.collatz_longest.restype = None
    return lib


_lib = _load()


def backend() -> str:
    """'c' se a biblioteca nativa foi carregada, senao 'python'."""
    return "c" if _lib else "python"


def _check(n: int) -> None:
    if n < 1:
        raise ValueError("n deve ser >= 1")


def steps_py(n: int) -> int:
    _check(n)
    count = 0
    while n != 1:
        n = n >> 1 if n % 2 == 0 else 3 * n + 1
        count += 1
    return count


def longest_py(limit: int) -> Tuple[int, int]:
    _check(limit)
    best_n, best_steps = 1, 0
    for n in range(2, limit + 1):
        s = steps_py(n)
        if s > best_steps:
            best_n, best_steps = n, s
    return best_n, best_steps


def steps_c(n: int) -> int:
    _check(n)
    if _lib is None:
        raise RuntimeError("biblioteca C nao encontrada (rode 'make')")
    result = _lib.collatz_steps(n)
    if result == _OVERFLOW:
        raise OverflowError("a sequencia estourou 64 bits; use o backend python")
    return result


def longest_c(limit: int) -> Tuple[int, int]:
    _check(limit)
    if _lib is None:
        raise RuntimeError("biblioteca C nao encontrada (rode 'make')")
    best_n, best_steps = ctypes.c_uint64(), ctypes.c_uint64()
    _lib.collatz_longest(limit, ctypes.byref(best_n), ctypes.byref(best_steps))
    if best_n.value == 0:
        raise OverflowError("a sequencia estourou 64 bits; use o backend python")
    return best_n.value, best_steps.value


def steps(n: int) -> int:
    """Usa C se disponivel; senao Python."""
    return steps_c(n) if _lib else steps_py(n)


def longest(limit: int) -> Tuple[int, int]:
    return longest_c(limit) if _lib else longest_py(limit)

import argparse
import time

from . import core


def _timed(fn, *args):
    t0 = time.perf_counter()
    result = fn(*args)
    return result, time.perf_counter() - t0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="collatz-bench", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("steps", help="passos de Collatz para um numero")
    s.add_argument("n", type=int)

    l = sub.add_parser("longest", help="maior sequencia ate LIMIT")
    l.add_argument("limit", type=int)
    l.add_argument("--backend", choices=["auto", "python", "c"], default="auto")

    b = sub.add_parser("bench", help="compara Python puro vs C")
    b.add_argument("limit", type=int, nargs="?", default=200_000)

    args = p.parse_args(argv)

    try:
        if args.cmd == "steps":
            print(f"{args.n} -> {core.steps(args.n)} passos  [{core.backend()}]")
        elif args.cmd == "longest":
            fn = {"auto": core.longest, "python": core.longest_py, "c": core.longest_c}[args.backend]
            (n, st), dt = _timed(fn, args.limit)
            print(f"maior sequencia ate {args.limit}: n={n} ({st} passos) em {dt:.3f}s")
        else:
            (py, t_py) = _timed(core.longest_py, args.limit)
            print(f"python : n={py[0]} ({py[1]} passos)  {t_py:.3f}s")
            if core.backend() != "c":
                print("c      : indisponivel (rode 'make' para compilar)")
                return 0
            (c, t_c) = _timed(core.longest_c, args.limit)
            print(f"c      : n={c[0]} ({c[1]} passos)  {t_c:.3f}s")
            assert py == c, "resultados divergentes!"
            print(f"speedup: {t_py / t_c:.0f}x")
    except (ValueError, OverflowError, RuntimeError) as e:
        print(f"erro: {e}")
        return 1
    return 0

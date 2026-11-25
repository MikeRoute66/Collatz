#!/usr/bin/env python3
"""Utilities for exploring the Collatz map.

This does not prove the Collatz conjecture. It gives exact, reproducible tools
for checking finite ranges and finding interesting stopping-time records.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Iterable


def step(n: int) -> int:
    """Return the next value in the Collatz trajectory."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    return n // 2 if n % 2 == 0 else 3 * n + 1


def trajectory(n: int) -> list[int]:
    """Return the full trajectory from n down to 1, including both endpoints."""
    if n < 1:
        raise ValueError("n must be a positive integer")

    values = [n]
    while n != 1:
        n = step(n)
        values.append(n)
    return values


_STOPPING_TIMES = {1: 0}


def stopping_time(n: int) -> int:
    """Return the number of Collatz steps needed for n to reach 1."""
    if n < 1:
        raise ValueError("n must be a positive integer")

    original = n
    path: list[int] = []
    while n not in _STOPPING_TIMES:
        path.append(n)
        n = step(n)

    known_time = _STOPPING_TIMES[n]
    for offset, value in enumerate(reversed(path), start=1):
        _STOPPING_TIMES[value] = known_time + offset

    return _STOPPING_TIMES[original]


def max_value(n: int) -> int:
    """Return the highest value reached by n's trajectory."""
    return max(trajectory(n))


@dataclass(frozen=True)
class Record:
    n: int
    stopping_time: int
    peak: int


def records(limit: int) -> list[Record]:
    """Return numbers <= limit that set a new stopping-time record."""
    if limit < 1:
        raise ValueError("limit must be a positive integer")

    best = -1
    found: list[Record] = []
    for n in range(1, limit + 1):
        time = stopping_time(n)
        if time > best:
            best = time
            found.append(Record(n=n, stopping_time=time, peak=max_value(n)))
    return found


def verify(limit: int) -> bool:
    """Verify that every n in [1, limit] reaches 1."""
    if limit < 1:
        raise ValueError("limit must be a positive integer")

    for n in range(1, limit + 1):
        stopping_time(n)
    return True


def format_records(items: Iterable[Record]) -> str:
    rows = ["n,stopping_time,peak"]
    rows.extend(f"{item.n},{item.stopping_time},{item.peak}" for item in items)
    return "\n".join(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Explore finite Collatz ranges.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    seq = subparsers.add_parser("sequence", help="print the trajectory for n")
    seq.add_argument("n", type=int)

    stat = subparsers.add_parser("stats", help="print stopping time and peak for n")
    stat.add_argument("n", type=int)

    check = subparsers.add_parser("verify", help="verify every n from 1 to limit")
    check.add_argument("limit", type=int)

    rec = subparsers.add_parser("records", help="print stopping-time records <= limit")
    rec.add_argument("limit", type=int)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "sequence":
        print(" ".join(str(value) for value in trajectory(args.n)))
    elif args.command == "stats":
        print(f"n={args.n}")
        print(f"stopping_time={stopping_time(args.n)}")
        print(f"peak={max_value(args.n)}")
    elif args.command == "verify":
        verify(args.limit)
        print(f"verified 1..{args.limit}")
    elif args.command == "records":
        print(format_records(records(args.limit)))
    else:
        raise AssertionError(f"unhandled command: {args.command}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

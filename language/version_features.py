"""Syntax introduced by Python 3.12. NOT part of the byte-identical domain.

This file exists so the parser-based tools in the roster meet syntax that
`src/` cannot contain -- the domain layer is held to the 3.6 language subset so
it can stay byte-identical across every family in the corpus.

PEP 695 (type parameter syntax), PEP 698 (@override) and PEP 701 (f-string
quoting) are all new in 3.12. Nothing here is imported by the domain; it is a
target, not a dependency.
"""
from collections.abc import Iterable
from itertools import batched
from typing import override

type Money = float                              # PEP 695 type alias


class Box[T]:                                   # PEP 695 class type parameter
    """A generic container. `T` is bound for the whole class body."""

    def __init__(self, item: T) -> None:
        self.item = item

    def get(self) -> T:
        return self.item


class LoudBox[T](Box[T]):
    @override                                   # PEP 698
    def get(self) -> T:
        return self.item


def first[T](items: Iterable[T]) -> T | None:   # PEP 695 function type parameter
    for item in items:
        return item
    return None


def in_chunks(values: list[int], size: int) -> list[tuple[int, ...]]:
    """itertools.batched is new in 3.12."""
    return list(batched(values, size))


def describe(rates: dict[str, Money]) -> str:
    """PEP 701: the outer quote character may be reused inside the expression."""
    return f"gold={rates["gold"]}"


def total(prices: list[Money]) -> Money:
    return sum(prices) if prices else 0.0

from typing import Iterable, Iterator, Callable
from hashlib import sha256
from functools import reduce


def dhash256(x: int) -> int:
    return sha256(sha256(x).digest()).digest()


def trunks(l: Iterable, n: int) -> Iterator:
    return zip(*[iter(l)] * n)


def concat(a: bytes, b: bytes) -> bytes:
    return bytes(a) + bytes(b)


def compose(*fs: Iterable[Callable]):
    def _(*args, **kwargs):
        return reduce(
            lambda x, y: y(x),
            fs,
            kwargs or args
        )
    return _


def to_sha256int(m: str):
    return int.from_bytes(sha256(m.encode()).digest(), 'big')

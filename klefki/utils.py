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


class EnumDict(dict):
    def __getattr__(self, k):
        '''
        Support Lazy
        '''
        value = self.get(k)
        if callable(value):
            value = value()
        if type(value) is dict:
            return EnumDict(value)
        else:
            return value

    def __setattr__(self, k, v):
        self.update({k: v})
        return self

    def __contains__(self, v):
        return v in self.values()

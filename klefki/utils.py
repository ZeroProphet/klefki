import base58
import base64
from typing import Iterable, Iterator, Callable
from klefki.types.algebra.isomorphism import bijection
from klefki.types.algebra.concrete import (
    FiniteFieldCyclicSecp256k1 as CF,
)

from hashlib import sha256
import hashlib
from functools import reduce

b58encode = bijection(base58.b58decode)(base58.b58encode)
b64encode = bijection(base64.b64decode)(base64.b64encode)


def int_to_byte(key: int) -> bytes:
    return key.to_bytes(32, byteorder='big')


@bijection(int_to_byte)
def byte_to_int(byte: bytes) -> CF:
    return int(byte.hex(), 16)


def dhash256(x: int) -> int:
    return sha256(sha256(x).digest()).digest()


def ripemd160(x) -> int:
    ripemd160 = hashlib.new('ripemd160')
    if isinstance(x, str):
        x = x.encode()
    if isinstance(x, list):
        for i in x:
            ripemd160.update(i)
    else:
        ripemd160.update(x)
    return ripemd160.digest()


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

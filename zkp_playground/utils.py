import base58
import base64
import sha3
from typing import Iterable, Iterator, Callable
from zkp_playground.algebra.isomorphism import bijection
from zkp_playground.curves.secp256k1 import (
    FiniteFieldCyclicSecp256k1 as CF,
)
import math
import hashlib
from hashlib import sha256
from functools import reduce

b58encode = bijection(base58.b58decode)(base58.b58encode)
b64encode = bijection(base64.b64decode)(base64.b64encode)


def int_to_byte(key: int, length=32) -> bytes:
    return key.to_bytes(length, byteorder='big')


def int_to_byte64(key: int) -> bytes:
    return int_to_byte(key, 64)


@bijection(int_to_byte)
def byte_to_int(byte: bytes) -> CF:
    return int.from_bytes(byte, "big")

def to_keccak256int(a: str) -> int:
    h = sha3.keccak_256()
    h.update(str.encode())
    return int.from_bytes(h.digest(), "big")


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


def parse_lv_format(b):
    i = 0
    j = i + 4
    ret = []
    while j <= len(b):
        l = int.from_bytes(bytes(b[i:j]), "big")
        i = j
        j = j + l
        v = bytes(b[i:j])
        ret.append(v)
        i = j
        j = i + 4
    return ret


def CF2Bytes(cf, l=32):
    return cf.value.to_bytes(l, byteorder="big")


def to_u32s(a: int, endian="little"):
    l = 32

    def split():
        carry = a
        while carry != 0:
            yield carry % 2**32
            carry = carry // (2 ** 32)

    return {
        "big": list(split())[::-1],
        "little": list(split())
    }[endian]


def from_u32s(a: list, endian="little"):
    ret = 0
    pos = 0
    if endian == "big":
        a = a[::-1]
    for i in a:
        ret += i * (2**(32*pos))
        pos += 1
    return ret


def from_u64s(a: list, endian="little"):
    ret = 0
    pos = 0
    if endian == "big":
        a = a[::-1]
    for i in a:
        ret += i * (2**(64*pos))
        pos += 1
    return ret


def to_u64s(a: int, endian="little"):
    l = 64

    def split():
        carry = a
        while carry != 0:
            yield carry % 2**64
            carry = carry // (2 ** 64)

    return {
        "big": list(map(hex, split()))[::-1],
        "little": list(map(hex, split()))
    }[endian]

from typing import Callable
from hashlib import sha256
from klefki.bitcoin.utils import b58encode

from klefki.crypto.ecsda import (
    random_privkey,
)
from klefki.types.algebra.concrete import (
    FiniteFieldCyclicBTC as CF,
)

from klefki.types.algebra.isomorphism import bijection, do


def int_to_byte(key: int) -> bytes:
    return key.to_bytes(32, byteorder='big')


@bijection(int_to_byte)
def byte_to_int(byte: bytes) -> CF:
    return int(byte.hex(), 16)


def wrap_key(key: bytes, version=123, compress=1):
    priv = bytes([version]) + key + bytes([compress])
    auth = sha256(sha256(priv).digest()).digest()[:4]
    res = priv + auth
    assert len(res) == 1 + 32 + 1 + 4
    return res


@bijection(wrap_key)
def unwrap_key(key: bytes):
    return key[1: -5]


def to_cf(a: int) -> CF:
    return CF(a)


@bijection(to_cf)
def from_cf(a: CF) ->int:
    return a.value


encode_privkey: Callable[[CF], str] = do(
    from_cf,
    int_to_byte,
    wrap_key,
    b58encode
)

decode_privkey: Callable[[str], CF] = ~encode_privkey


def gen_random_privkey():
    return encode_privkey(random_privkey())

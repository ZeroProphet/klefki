from typing import Callable
from hashlib import sha256
from zkp_playground.utils import b58encode, int_to_byte

from zkp_playground.crypto.ecdsa.secp256k1 import (
    random_privkey,
)
from zkp_playground.algebra.concrete import (
    FiniteFieldCyclicSecp256k1 as CF,
)

from zkp_playground.algebra.isomorphism import bijection, do


def wrap_key(key: bytes, version=128, compress=1):
    priv = bytes([version]) + key + bytes([compress])
    auth = sha256(sha256(priv).digest()).digest()[:4]
    res = priv + auth
    assert len(res) == 1 + 32 + 1 + 4
    return res


@bijection(wrap_key)
def unwrap_key(key: bytes):
    return key[1: -5]


def to_cf(a: int):
    return CF(a)


@bijection(to_cf)
def from_cf(a: CF) -> int:
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

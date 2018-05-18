import hashlib
from typing import Callable
from klefki.bitcoin.utils import b58encode, int_to_byte
from klefki.crypto.ecdsa import (
    random_privkey,
)
from klefki.types.algebra.concrete import (
    FiniteFieldCyclicSecp256k1 as CF,
)

from klefki.types.algebra.isomorphism import bijection, do


@bijection(CF)
def from_cf(a: CF) -> int:
    return a.value


def add_version(a: bytes) -> bytes:
    return bytes([80]) + a


@bijection(add_version)
def remove_version(a: bytes) -> bytes:
    return a[1:]


def add_checksum(a: bytes) -> bytes:
    return a + hashlib.sha256(hashlib.sha256().digest()).digest()[:4]


@bijection(add_checksum)
def remove_checksum(a: bytes) -> bytes:
    return a[-4:]


encode_privkey: Callable[[CF], str] = do(
    from_cf,
    int_to_byte,
    add_version,
    b58encode
)

decode_privkey: Callable[[str], CF] = ~encode_privkey


def gen_random_privkey():
    return encode_privkey(random_privkey())

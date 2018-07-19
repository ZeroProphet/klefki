import hashlib
from typing import Callable
from klefki.utils import b58encode, int_to_byte
from klefki.crypto.ecdsa.secp256k1 import (
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
    return bytes([0x80]) + a


@bijection(add_version)
def remove_version(a: bytes) -> bytes:
    _a = bytearray(a)
    assert hex(_a[0]) == '0x80'
    return _a[1:]


def add_checksum(a: bytes) -> bytes:
    assert len(a) == 33
    return a + hashlib.sha256(hashlib.sha256(a).digest()).digest()[:4]


@bijection(add_checksum)
def remove_checksum(a: bytes) -> bytes:
    res = bytes(bytearray(a)[:-4])
    checksum = bytes(bytearray(a)[-4:])
    new_checksum = hashlib.sha256(hashlib.sha256(res).digest()).digest()[:4]
    assert checksum == new_checksum
    return res


encode_privkey: Callable[[CF], str] = do(
    from_cf,
    int_to_byte,
    add_version,
    add_checksum,
    b58encode
)

decode_privkey: Callable[[str], CF] = ~encode_privkey


def gen_random_privkey():
    return encode_privkey(random_privkey())

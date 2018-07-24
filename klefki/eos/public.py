from klefki.utils import int_to_byte
from klefki.crypto.ecdsa.secp256k1 import pubkey
from klefki.types.algebra.concrete import (
    EllipticCurveGroupSecp256k1 as ECG,
    FiniteFieldCyclicSecp256k1 as CF

)
from klefki.types.algebra.isomorphism import bijection, do
from klefki.utils import ripemd160, b58encode, byte_to_int


def to_bytes(pub: ECG) -> str:
    return bytes([2 + (pub.value[1].value % 2)]) + int_to_byte(pub.value[0].value)

@bijection(to_bytes)
def from_bytes(a):
    return ECG([
        CF(byte_to_int(a[:1]) - 2),
        CF(byte_to_int(a[1:]))
    ])


def checksum(a) -> int:
    assert len(a) == 33
    return 'EOS' + b58encode(a + ripemd160(a)[:4])

@bijection(checksum)
def unchecksum(a):
    return b58encode.inverse(a[3:])


def gen_pub_key(key: CF):
    return checksum(to_bytes(pubkey(key)))

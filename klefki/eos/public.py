from klefki.utils import int_to_byte
from klefki.crypto.ecdsa import pubkey
from klefki.types.algebra.concrete import (
    EllipticCurveGroupSecp256k1 as ECG,
    FiniteFieldCyclicSecp256k1 as CF

)
from klefki.utils import ripemd160, b58encode


def to_bytes(pub: ECG) -> str:
    return bytes([2 + (pub.value[1].value % 2)]) + int_to_byte(pub.value[0].value)


def checksum(a) -> int:
    assert len(a) == 33
    return 'EOS' + b58encode(a + ripemd160(a)[:4])


def gen_pub_key(key: CF):
    return checksum(to_bytes(pubkey(key)))

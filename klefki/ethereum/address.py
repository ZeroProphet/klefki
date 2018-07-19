from sha3 import keccak_256
from klefki.crypto.ecdsa.secp256k1 import pubkey
from klefki.utils import int_to_byte
from klefki.types.algebra.concrete import (
    EllipticCurveGroupSecp256k1 as ECG,
    FiniteFieldCyclicSecp256k1 as CF,
)


def gen_address(pub: ECG) -> str:
    x = int_to_byte(pub.value[0].value)
    y = int_to_byte(pub.value[1].value)
    return gen_address_from_bytes(x + y)


def gen_address_from_bytes(pub: bytes) -> str:
    return '0x%s' % keccak_256(pub).hexdigest()[24:].upper()


def gen_address_from_priv(priv: CF) -> str:
    return gen_address(pubkey(priv))

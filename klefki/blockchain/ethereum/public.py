from klefki.crypto.ecdsa.secp256k1 import pubkey
from klefki.types.algebra.concrete import (
    EllipticCurveGroupSecp256k1 as ECG,
    FiniteFieldCyclicSecp256k1 as CF,
    FiniteFieldSecp256k1 as F
)
from klefki.types.algebra.isomorphism import bijection


def encode_pubkey(key: ECG):
    x = hex(key.value[0].value)[2:]
    y = hex(key.value[1].value)[2:]
    return '0' * (32 - len(x)) + x + '0' * (32 - len(y)) + y


@bijection(encode_pubkey)
def decode_pubkey(key: str) -> ECG:
    x = F(int(key[:32], 16))
    y = F(int(key[32:], 16))
    return ECG((x, y))


def gen_pub_key(key: CF) -> str:
    return encode_pubkey(
        pubkey(key)
    )

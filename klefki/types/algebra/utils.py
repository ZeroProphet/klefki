from klefki.types.algebra.concrete import (
    EllipticCurveGroupSecp256k1 as ECG,
    FiniteFieldCyclicSecp256k1 as CF,
    FiniteFieldSecp256k1 as F
)
from klefki.types.algebra.isomorphism import bijection
from random import randint

def encode(key: ECG):
    x = hex(key.value[0].value)[2:]
    y = hex(key.value[1].value)[2:]
    return '0' * (32 - len(x)) + x + '0' * (32 - len(y)) + y


@bijection(encode)
def decode(key: str) -> ECG:
    x = F(int(key[:32], 16))
    y = F(int(key[32:], 16))
    return ECG((x, y))


def randfield(F):
    return F(randint(0, F.P - 1))

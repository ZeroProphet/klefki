from functools import reduce
from klefki.crypto.ecdsa.secp256k1 import (
    pubkey
)

from klefki.types.algebra.concrete import (
    EllipticCurveGroupSecp256k1 as ECG,
    EllipticCurveCyclicSubgroupSecp256k1 as CG,
    FiniteFieldSecp256k1 as F,
    FiniteFieldCyclicSecp256k1 as CF
)
from klefki.types.algebra.isomorphism import bijection


G = CG.G
A = ECG.A
B = ECG.B
P = F.P


def encode_pubkey(pub: ECG) -> str:
    n = hex(pub.value[0].value).replace('0x', '')
    return '0' + str(2 + (pub.value[1].value % 2)) + ((64 - len(n)) * '0' + n)


@bijection(encode_pubkey)
def decode_pubkey(pub: str) -> ECG:
    pub = bytearray.fromhex(pub)
    x = reduce(lambda x, y: x * 256 + y, bytes(pub[1:33]), 0)
    beta = pow(int(x * x * x + A * x + B), int((P + 1) // 4), int(P))
    y = (P - beta) if ((beta + pub[0]) % 2) else beta
    return ECG(
        (
            F(x),
            F(y)
        )
    )


def gen_pub_key(key: CF) -> str:
    return encode_pubkey(
        pubkey(key)
    )

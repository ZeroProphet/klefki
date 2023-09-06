from functools import reduce
from zkp_playground.crypto.ecdsa.secp256k1 import (
    pubkey
)

from zkp_playground.algebra.concrete import (
    EllipticCurveGroupSecp256k1 as CG,
    FiniteFieldSecp256k1 as F,
    FiniteFieldCyclicSecp256k1 as CF
)
from zkp_playground.algebra.isomorphism import bijection


G = CG.G
A = CG.A
B = CG.B
P = F.P


def encode_pubkey(pub: CG) -> str:
    n = hex(pub.value[0].value).replace('0x', '')
    return '0' + str(2 + (pub.value[1].value % 2)) + ((64 - len(n)) * '0' + n)


@bijection(encode_pubkey)
def decode_pubkey(pub: str) -> CG:
    pub = bytearray.fromhex(pub)
    x = reduce(lambda x, y: x * 256 + y, bytes(pub[1:33]), 0)
    beta = pow(int(x * x * x + A * x + B), int((P + 1) // 4), int(P))
    y = (P - beta) if ((beta + pub[0]) % 2) else beta
    return CG(
        (
            F(x),
            F(y)
        )
    )


def gen_pub_key(key: CF) -> str:
    return encode_pubkey(
        pubkey(key)
    )

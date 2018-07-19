from hashlib import sha256
from klefki.utils import dhash256, ripemd160, b58encode
from klefki.crypto.ecdsa.secp256k1 import (
    pubkey
)
from klefki.types.algebra.concrete import (
    EllipticCurveGroupSecp256k1 as ECG,
    EllipticCurveCyclicSubgroupSecp256k1 as CG,
    FiniteFieldSecp256k1 as F
)

__all__ = [
    'gen_address'
]


G = CG.G
A = ECG.A
B = ECG.B
P = F.P


def gen_address(pub: ECG) -> str:
    x, y = pub.value[0].value, pub.value[1].value
    if y % 2 == 0:
        prefix = bytes([0x02])
    else:
        prefix = bytes([0x03])
    networkid = bytes([0x00])
    hashed = ripemd160(
        sha256(
            prefix + x.to_bytes(32, byteorder='big')
        ).digest()
    )
    assert len(hashed) == 20
    with_network = networkid + hashed
    auth = dhash256(with_network)[:4]
    res = with_network + auth
    assert len(res) == 25
    return b58encode(res)


def gen_address_from_priv(key) -> str:
    return gen_address(pubkey(key))

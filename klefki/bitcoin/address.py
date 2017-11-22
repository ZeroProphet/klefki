from hashlib import sha256
import hashlib
import base58
from klefki.crypto.ecdsa import (
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
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(
        sha256(
            prefix + x.to_bytes(32, byteorder='big')
        ).digest()
    )
    hashed = ripemd160.digest()
    assert len(hashed) == 20
    with_network = networkid + hashed
    auth = sha256(sha256(with_network).digest()).digest()[:4]
    res = with_network + auth
    assert len(res) == 25
    return base58.b58encode(res)


def gen_address_from_key(key) -> str:
    return gen_address(pubkey(key))

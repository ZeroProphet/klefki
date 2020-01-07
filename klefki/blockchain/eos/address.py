import hashlib
from klefki.crypto.ecdsa.secp256k1 import pubkey
from klefki.types.algebra.concrete import (
    EllipticCurveGroupSecp256k1 as ECG,
    FiniteFieldCyclicSecp256k1 as CF,
)
from klefki.utils import ripemd160, b58encode


from .public import to_bytes


def gen_address(pub: ECG):
    pub = to_bytes(pub)
    pub_sha = hashlib.sha512(pub).digest()
    addy = ripemd160(pub_sha)
    return 'EOS' + b58encode(addy + ripemd160(addy)[:4])


def gen_address_from_priv(priv: CF) -> str:
    return gen_address(pubkey(priv))

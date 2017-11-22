from sha3 import keccak_256
from .public import encode_pubkey
from klefki.types.algebra.concrete import (
    EllipticCurveGroupSecp256k1 as ECG,
)


def gen_address(pub: ECG) -> str:
    return gen_address_from_str(pub)


def gen_address_from_str(pub: str) -> str:
    return keccak_256(pub).hexdigest

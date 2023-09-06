from zkp_playground.crypto.ecdsa.secp256k1 import (
    random_privkey,
)
from zkp_playground.algebra.concrete import (
    FiniteFieldCyclicSecp256k1 as CF,
)
from zkp_playground.algebra.isomorphism import bijection


def encode_privkey(key: CF) -> str:
    return hex(key.value)[2:]


@bijection(encode_privkey)
def decode_privkey(key: str) -> CF:
    return CF(int(key, 16))


def gen_random_privkey():
    return random_privkey()

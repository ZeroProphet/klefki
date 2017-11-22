import base64
import base58
from klefki.types.algebra.isomorphism import bijection
from klefki.types.algebra.concrete import (
    FiniteFieldCyclicSecp256k1 as CF,
)


b58encode = bijection(base58.b58decode)(base58.b58encode)
b64encode = bijection(base64.b64decode)(base64.b64encode)


def int_to_byte(key: int) -> bytes:
    return key.to_bytes(32, byteorder='big')


@bijection(int_to_byte)
def byte_to_int(byte: bytes) -> CF:
    return int(byte.hex(), 16)

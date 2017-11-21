from functools import reduce
from hashlib import sha256
import hashlib
import base58
from klefki.crypto.ecsda import (
    random_privkey,
    pubkey
)
from klefki.types.algebra.concrete import (
    EllipticCurveGroupBTC as ECG,
    FiniteFieldCyclicBTC as CF,
    EllipticCurveCyclicSubgroupBTC as CG,
    FiniteFieldBTC as F
)
from klefki.types.algebra.isomorphism import bijection

__all__ = [
    'encode_pubkey',
    'decode_pubkey',
    'encode_privkey',
    'decode_privkey',
    'gen_pub_key',
    'gen_key_pair',
    'gen_address'
]


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


def encode_privkey(key: CF, version=128, compress=1) -> str:
    private_key = bytes([version]) + key_to_byte(key) + bytes([compress])
    auth = sha256(sha256(private_key).digest()).digest()[:4]
    res = private_key + auth
    assert len(res) == 1 + 32 + 1 + 4
    return base58.b58encode(res)


@bijection(encode_privkey)
def decode_privkey(key: str) -> CF:
    return CF(int(base58.b58decode(key)[1: -5].hex(), 16))


def gen_random_privkey():
    return encode_privkey(random_privkey())


def key_to_byte(key: CF):
    return key.value.to_bytes(32, byteorder='big')


def gen_pub_key(key: CF) -> str:
    return encode_pubkey(
        pubkey(key)
    )


def gen_key_pair(key=random_privkey()):
    return encode_privkey(key), gen_pub_key(key)


def gen_address(key: CF):
    pub = pubkey(key)
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

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


G = CG.G
A = ECG.A
B = ECG.B
P = F.P


def encode_pub(pub: ECG) -> str:
    n = hex(pub.value[0].value).replace('0x', '')
    return '0' + str(2 + (pub.value[1].value % 2)) + ((64 - len(n)) * '0' + n)


def decode_pub(pub: str) -> ECG:
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


def gen_random_privkey():
    return gen_priv_key(random_privkey())


def gen_priv_key(key: CF, version=128, compress=1) -> str:
    private_key = bytes([version]) + key.value.to_bytes(
        32, byteorder='big') + bytes([compress])
    auth = sha256(sha256(private_key).digest()).digest()[:4]
    res = private_key + auth
    assert len(res) == 1 + 32 + 1 + 4
    return base58.b58encode(res)


def key_to_byte(key: CF):
    key.value.to_bytes(32, byteorder='big')


def gen_pub_key(key: CF) -> str:
    return encode_pub(
        pubkey(key)
    )


def gen_key_pair(key=random_privkey()):
    return gen_priv_key(key), gen_pub_key(key)


def gen_address(key: CF):
    pub = G @ key
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

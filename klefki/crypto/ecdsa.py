from typing import Tuple
import random
from klefki.utils import to_sha256int
from klefki.types.algebra.concrete import (
    JacobianGroupSecp256k1 as JG,
    FiniteFieldSecp256k1 as F,
    EllipticCurveCyclicSubgroupSecp256k1 as CG,
    EllipticCurveGroupSecp256k1 as ECG,
    FiniteFieldCyclicSecp256k1 as CF
)

__all__ = [
    'random_privkey',
    'pubkey',
    'sign',
    'verify',
    'verify_msghash'

]

N = CG.N
G = CG.G
A = ECG.A
B = ECG.B
P = F.P

SigType = Tuple[CF, CF, CF]


def random_privkey() -> CF:
    return CF(random.randint(1, N))


def pubkey(priv: CF) -> ECG:
    return ECG(JG(G @ priv))


def sign(priv: CF, m: str) -> SigType:
    '''
    https://bitcoin.stackexchange.com/questions/38351/ecdsa-v-r-s-what-is-v
    '''
    k = CF(random_privkey())
    z = CF(to_sha256int(m))

    p = G @ k
    r, y = CF(p.value[0]), CF(p.value[1])
    s = (z + priv * r) / k
    v = CF(27 + y.value % 2)
    return v, r, s


def verify(pub: ECG, sig: tuple, msg: str):
    mhash = to_sha256int(msg)
    return verify_msghash(pub, sig, mhash)


def verify_msghash(pub: ECG, sig: tuple, mhash: int):
    if len(sig) == 2:
        r, s = sig
    else:
        v, r, s = sig
    z = CF(mhash)
    u1 = z / s
    u2 = r / s
    rp = G @ u1 + pub @ u2
    return r == rp.value[0]


def recover(sig: tuple, mhash: int):
    v, r, s = sig
    x = F(r)
    xcubedaxb = x ** 3 + F(A) * x + F(B)
    beta = pow(xcubedaxb.value, (P + 1) // 4, P)
    if v.value % 2 ^ beta % 2:
        y = beta
        print('case 1')
    else:
        print('case 2')
        y = P - beta
    Gz = G @ (F(N) - F(mhash))
    Xy = ECG((F(x), F(y))) @ s
    Qr = Gz + Xy
    Q = Qr @ ~CF(r)
    return Q


def recover_via_msg(sig: tuple, msg: str):
    return recover(sig, to_sha256int(msg))


def proof():
    priv = random_privkey()
    m = 'test'
    k = CF(random_privkey())
    z = CF(to_sha256int(m))
    r = CF((G @ k).value[0])
    s = z / k + priv * r / k

    assert k == z / s + priv * r / s
    assert G @ k == G @ (z / s + priv * r / s)
    assert G @ k == G @ (z / s) + G @ priv @ (r / s)

    pub = G @ priv
    assert pub == pubkey(priv)
    assert G @ k == G @ (z / s) + pub @ (r / s)
    u1 = z / s
    u2 = r / s
    assert G @ k == G @ u1 + pub @ u2

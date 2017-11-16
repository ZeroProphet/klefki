import random
from klefki.utils import to_sha256int
from klefki.types.algebra.concrete import (
    JacobianGroupBTC as JG,
    EllipticCurveCyclicSubgroupBTC as CG,
    EllipticCurveGroupBTC as ECG,
    FiniteFieldCyclicBTC as CF
)

N = CG.N
G = CG.G


def random_privkey() -> CF:
    return CF(random.randint(1, N))


def pubkey(priv: CF) -> ECG:
    return ECG(JG(G @ priv))


def sign(priv: CF, m: str) -> tuple:
    k = CF(random_privkey())
    z = CF(to_sha256int(m))
    r = CF((G @ k).value[0])  # From BTCField to CyclicBTCField
    s = z / k + priv * r / k
    return r, s


def verify(pub: ECG, sig: tuple, m: str):
    r, s = sig
    z = CF(to_sha256int(m))
    u1 = z / s
    u2 = r / s
    rp = G @ u1 + pub @ u2
    return r == rp.value[0]


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

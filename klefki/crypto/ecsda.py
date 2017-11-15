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


def random_privkey() -> int:
    return CF(random.randint(1, N))


def pubkey(priv: CF) -> ECG:
    return ECG(JG(G @ priv))


def sign(priv: CF, m: str) -> tuple:
    k = CF(random_privkey())
    z = CF(to_sha256int(m))
    priv = CF(priv)
    r = CF((G @ k).value[0])  # From BTCField to CyclicBTCField
    s = z / k + priv * r / k
    return r, s


def verify(pub: ECG, sig: tuple, m: str):
    r, s = sig
    z = CF(to_sha256int(m))
    u1 = CF(z) / s
    u2 = r / s
    rp = G @ u1 + pub @ u2
    return r == rp.value[0]

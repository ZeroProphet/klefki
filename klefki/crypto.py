import hashlib
from klefki.address import gen_random_number
from klefki.types.algebra.concrete import (
    EllipticCurveCyclicSubgroupBTC,
    EllipticCurveGroupBTC,
    FiniteFieldBTC
)

G = EllipticCurveCyclicSubgroupBTC.G
A = EllipticCurveGroupBTC.A
B = EllipticCurveGroupBTC.B
P = FiniteFieldBTC.P


# REF: https://www.cryptocompare.com/wallets/guides/how-do-digital-signatures-in-bitcoin-work/


def sign(m: str, priv):
    mh = FiniteFieldBTC(int.from_bytes(
        hashlib.sha256(m.encode()).digest(), 'big'))
    mp = G @ EllipticCurveCyclicSubgroupBTC(mh)
    rn = FiniteFieldBTC(gen_random_number())
    rp = G @ EllipticCurveCyclicSubgroupBTC(rn)
    pu = G @ EllipticCurveCyclicSubgroupBTC((mp.value[0] * priv))
    return (
        EllipticCurveCyclicSubgroupBTC(pu.value[0]),
        EllipticCurveCyclicSubgroupBTC((mh + rp.value[0] * priv) / rn)
    )


def verify(m: str, pub, sig):
    xr, sf = sig
    hs = FiniteFieldBTC(int.from_bytes(
        hashlib.sha256(m.encode()).digest(), 'big'))
    u1 = EllipticCurveCyclicSubgroupBTC(hs / sf.value)
    u2 = EllipticCurveCyclicSubgroupBTC(xr.value / sf.value)
    res = (G @ u1 + pub @ u2)
    return xr == res.value[0]

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


def sign(m: str, priv):
    # https://www.cryptocompare.com/wallets/guides/how-do-digital-signatures-in-bitcoin-work/
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

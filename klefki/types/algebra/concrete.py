from .groups import EllipticCurveGroup, CyclicGroup, JacobianGroup
from .fields import FiniteField
import klefki.const as const

__all__ = [
    'FiniteFieldBTC',
    'EllipticCurveGroupBTC',
    'JacobianGroupBTC',
    'EllipticCurveCyclicSubgroupBTC'
]


class FiniteFieldBTC(FiniteField):
    __slots__ = ()
    P = 2**256 - 2**32 - 977


class EllipticCurveGroupBTC(EllipticCurveGroup):
    __slots__ = ()
    A = 0
    B = 7


class JacobianGroupBTC(JacobianGroup):
    __slots__ = ()
    A = 0
    B = 7


class EllipticCurveCyclicSubgroupBTC(CyclicGroup):
    __slots__ = ()
    G = EllipticCurveGroupBTC(
        (
            FiniteFieldBTC(const.Gx),
            FiniteFieldBTC(const.Gy)
        )
    )
    N = const.N

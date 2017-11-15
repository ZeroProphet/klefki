from .groups import EllipticCurveGroup, CyclicGroup, JacobianGroup
from .fields import FiniteField
import klefki.const as const

__all__ = [
    'FiniteFieldBTC',
    'FiniteFieldCyclicBTC',
    'EllipticCurveGroupBTC',
    'JacobianGroupBTC',
    'EllipticCurveCyclicSubgroupBTC'
]


class FiniteFieldBTC(FiniteField):
    __slots__ = ()
    P = const.P


class FiniteFieldCyclicBTC(FiniteField):
    __slots__ = ()
    P = const.N


class EllipticCurveGroupBTC(EllipticCurveGroup):
    __slots__ = ()
    A = const.A
    B = const.B


class JacobianGroupBTC(JacobianGroup):
    __slots__ = ()
    A = const.A
    B = const.B


class EllipticCurveCyclicSubgroupBTC(CyclicGroup):
    __slots__ = ()
    G = EllipticCurveGroupBTC(
        (
            FiniteFieldBTC(const.Gx),
            FiniteFieldBTC(const.Gy)
        )
    )
    N = const.N

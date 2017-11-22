from .groups import EllipticCurveGroup, CyclicGroup, JacobianGroup
from .fields import FiniteField
import klefki.const as const

__all__ = [
    'FiniteFieldSecp256k1',
    'FiniteFieldCyclicSecp256k1',
    'EllipticCurveGroupSecp256k1',
    'JacobianGroupSecp256k1',
    'EllipticCurveCyclicSubgroupSecp256k1'
]


class FiniteFieldSecp256k1(FiniteField):
    __slots__ = ()
    P = const.P


class FiniteFieldCyclicSecp256k1(FiniteField):
    __slots__ = ()
    P = const.N


class EllipticCurveGroupSecp256k1(EllipticCurveGroup):
    __slots__ = ()
    A = const.A
    B = const.B


class JacobianGroupSecp256k1(JacobianGroup):
    __slots__ = ()
    A = const.A
    B = const.B


class EllipticCurveCyclicSubgroupSecp256k1(CyclicGroup):
    __slots__ = ()
    G = EllipticCurveGroupSecp256k1(
        (
            FiniteFieldSecp256k1(const.Gx),
            FiniteFieldSecp256k1(const.Gy)
        )
    )
    N = const.N

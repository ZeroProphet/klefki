from zkp_playground.algebra.groups import EllipticCurveGroup, EllipicCyclicSubgroup, JacobianGroup
from zkp_playground.algebra.fields import FiniteField
import zkp_playground.const as const

__all__ = [
    'FiniteFieldSecp256k1',
    'FiniteFieldCyclicSecp256k1',
    'EllipticCurveGroupSecp256k1',
    'JacobianGroupSecp256k1',
    # 'EllipticCurveCyclicSubgroupSecp256k1',
    'FiniteFieldSecp256r1',
    'FiniteFieldCyclicSecp256r1',
    'EllipticCurveGroupSecp256r1',
    'JacobianGroupSecp256r1',
    'EllipticCurveCyclicSubgroupSecp256r1'

]

from zkp_playground.curves.secp256k1 import (
    FiniteFieldSecp256k1,
    FiniteFieldCyclicSecp256k1,
    EllipticCurveGroupSecp256k1
)


class JacobianGroupSecp256k1(JacobianGroup):
    __slots__ = ()
    A = const.SECP256K1_A
    B = const.SECP256K1_B


class FiniteFieldSecp256r1(FiniteField):
    __slots__ = ()
    P = const.SECP256R1_P


class FiniteFieldCyclicSecp256r1(FiniteField):
    __slots__ = ()
    P = const.SECP256R1_N


class EllipticCurveGroupSecp256r1(EllipticCurveGroup):
    __slots__ = ()
    A = const.SECP256R1_A
    B = const.SECP256R1_B


class JacobianGroupSecp256r1(JacobianGroup):
    __slots__ = ()
    A = const.SECP256R1_A
    B = const.SECP256R1_B


class EllipticCurveCyclicSubgroupSecp256r1(EllipicCyclicSubgroup):
    N = const.SECP256R1_N
    A = const.SECP256R1_A
    B = const.SECP256R1_B


class EllipticCurveGroupSecp256r1(EllipticCurveGroup):
    A = const.SECP256R1_A
    B = const.SECP256R1_B
    G = EllipticCurveCyclicSubgroupSecp256r1(
        (
            FiniteFieldSecp256k1(const.SECP256R1_Gx),
            FiniteFieldSecp256k1(const.SECP256R1_Gy)
        )
    )

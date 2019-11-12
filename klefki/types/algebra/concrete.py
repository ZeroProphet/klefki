from .groups import EllipticCurveGroup, EllipicCyclicSubroup, JacobianGroup
from .fields import FiniteField
import klefki.const as const

__all__ = [
    'FiniteFieldSecp256k1',
    'FiniteFieldCyclicSecp256k1',
    'EllipticCurveGroupSecp256k1',
    'JacobianGroupSecp256k1',
    'EllipticCurveCyclicSubgroupSecp256k1',
    'FiniteFieldSecp256r1',
    'FiniteFieldCyclicSecp256r1',
    'EllipticCurveGroupSecp256r1',
    'JacobianGroupSecp256r1',
    'EllipticCurveCyclicSubgroupSecp256r1'

]


class FiniteFieldSecp256k1(FiniteField):
    P = const.SECP256K1_P


class FiniteFieldCyclicSecp256k1(FiniteField):
    P = const.SECP256K1_N


class EllipticCurveCyclicSubgroupSecp256k1(EllipicCyclicSubroup):
    N = const.SECP256K1_N
    A = const.SECP256K1_A
    B = const.SECP256K1_B

    @property
    def x(self):
        return self.value[0]

    @property
    def y(self):
        return self.value[1]


class EllipticCurveGroupSecp256k1(EllipticCurveGroup):
    A = const.SECP256K1_A
    B = const.SECP256K1_B
    G = EllipticCurveCyclicSubgroupSecp256k1(
        (
            FiniteFieldSecp256k1(const.SECP256K1_Gx),
            FiniteFieldSecp256k1(const.SECP256K1_Gy)
        )
    )

    @property
    def x(self):
        return self.value[0]

    @property
    def y(self):
        return self.value[1]


EllipticCurveCyclicSubgroupSecp256k1.G = EllipticCurveGroupSecp256k1.G


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


class EllipticCurveCyclicSubgroupSecp256r1(EllipicCyclicSubroup):
    N = const.SECP256R1_N
    A = const.SECP256R1_A
    B = const.SECP256R1_B

    @property
    def x(self):
        return self.value[0]

    @property
    def y(self):
        return self.value[1]

class EllipticCurveGroupSecp256r1(EllipticCurveGroup):
    A = const.SECP256R1_A
    B = const.SECP256R1_B
    G = EllipticCurveCyclicSubgroupSecp256r1(
        (
            FiniteFieldSecp256k1(const.SECP256R1_Gx),
            FiniteFieldSecp256k1(const.SECP256R1_Gy)
        )
    )

    @property
    def x(self):
        return self.value[0]

    @property
    def y(self):
        return self.value[1]



EllipticCurveCyclicSubgroupSecp256r1.G = EllipticCurveGroupSecp256r1.G

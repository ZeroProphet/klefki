import klefki.const as const
from klefki.types.algebra.fields import FiniteField
from klefki.types.algebra.groups import EllipticCurveGroup
from klefki.types.algebra.groups import EllipicCyclicSubgroup


class FiniteFieldSecp256k1(FiniteField):
    P = const.SECP256K1_P


class FiniteFieldCyclicSecp256k1(FiniteField):
    P = const.SECP256K1_N


class EllipticCurveGroupSecp256k1(EllipticCurveGroup):
    N = const.SECP256K1_N
    A = const.SECP256K1_A
    B = const.SECP256K1_B

    @property
    def x(self):
        return self.value[0]

    @property
    def y(self):
        return self.value[1]


EllipticCurveGroupSecp256k1.G = EllipticCurveGroupSecp256k1(
    (
        FiniteFieldSecp256k1(const.SECP256K1_Gx),
        FiniteFieldSecp256k1(const.SECP256K1_Gy)
    )
)

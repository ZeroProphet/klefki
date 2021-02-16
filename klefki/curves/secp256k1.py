import klefki.const as const
from klefki.algebra.fields import FiniteField
from klefki.algebra.groups import EllipticCurveGroup
from klefki.algebra.groups import EllipicCyclicSubgroup
from klefki.curves.arith import short_weierstrass_form_curve_addition2


class FiniteFieldSecp256k1(FiniteField):
    P = const.SECP256K1_P


class FiniteFieldCyclicSecp256k1(FiniteField):
    P = const.SECP256K1_N


class EllipticCurveGroupSecp256k1(EllipticCurveGroup):
    """
    y^2 = x^3 + A * x + B
    """

    N = const.SECP256K1_N
    A = const.SECP256K1_A
    B = const.SECP256K1_B

    def op(self, g):
        field = self.id[0].__class__
        x, y = short_weierstrass_form_curve_addition2(
            self.x, self.y,
            g.x, g.y,
            field.zero(),
            field.zero(),
            field.zero(),
            field(self.A),
            field(self.B),
            field
        )
        if x == y == field(0):
            return self.__class__(0)
        return self.__class__((x, y))

    @classmethod
    def lift_x(cls, x: FiniteField):
        F = x.__class__
#        y = (x**3 + F(cls.A) * x + F(cls.B))**(1/2)
        y = (x**3 + x*F(cls.A) + F(cls.B))**(1/2)
        return cls((x, y))


EllipticCurveGroupSecp256k1.G = EllipticCurveGroupSecp256k1(
    (
        FiniteFieldSecp256k1(const.SECP256K1_Gx),
        FiniteFieldSecp256k1(const.SECP256K1_Gy)
    )
)

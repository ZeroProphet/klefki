import zkp_playground.const as const
from zkp_playground.algebra.fields import FiniteField
from zkp_playground.algebra.groups import EllipticCurveGroup
from zkp_playground.algebra.groups import EllipicCyclicSubgroup
from zkp_playground.curves.arith import short_weierstrass_form_curve_addition


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
        x, y = short_weierstrass_form_curve_addition(
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

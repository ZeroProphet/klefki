"""
ref: https://github.com/ethereum/research/blob/711bd9532b4534ef5ae6277bd7afe625195506d5/zksnark/bn128_field_elements.py
"""
import klefki.const as const
from klefki.types.algebra.fields import FiniteField
from klefki.types.algebra.fields import PolyExtField
from klefki.types.algebra.groups import EllipticCurveGroup
from klefki.types.algebra.groups import EllipicCyclicSubgroup
from klefki.curves.arith import short_weierstrass_form_curve_addition2


class BN128FP(FiniteField):
    P = const.BN128_P


class BN128FP2(PolyExtField):
    F = BN128FP
    E = const.BN128_FP2_E


class BN128FP12(PolyExtField):
    F = BN128FP
    E = const.BN128_FP12_E


class ECGBN128(EllipticCurveGroup):
    A = const.BN128_A
    B = const.BN128_B

    def op(self, g):
        if g == self.zero():
            return self
        if self == self.zero():
            return g
        field = self.id[0].type

        # a1,a3,a2,a4,a6 = 0, 0, 0, a, b
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
        if x == y == field.zero():
            return self.zero()
        return self.__class__((x, y))

    def twist(self):
        x, y = self.x, self.y
        if isinstance(x, BN128FP12) and isinstance(y, BN128FP12):
            return self
        elif isinstance(x, BN128FP2) and isinstance(y, BN128FP2):
            return self.twist_FP2_to_FP12(x, y)
        elif isinstance(x, BN128FP) and isinstance(y, BN128FP):
            return self.twist_FP_to_FP12(x, y)
        else:
            raise Exception("cannot twist curve to fp12")

    @classmethod
    def twist_FP_to_FP12(cls, x, y):
        return cls(BN128FP12([x] + [BN128FP.zero()] * 11), BN128FP12([y] + [BN128FP.zero()] * 11))

    @classmethod
    def twist_FP2_to_FP12(cls, x, y):
        # "Twist" a point in E(FQ2) into a point in E(FQ12)
        zero = BN128FP.zero()
        one = BN128FP.one()
        w = BN128FP12([zero, one] + [zero] * 10)
        assert isinstance(x, BN128FP2)
        assert isinstance(y, BN128FP2)
        nx = BN128FP12([x.id[0]] + [zero] * 5 + [x.id[1]] + [zero] * 5)
        ny = BN128FP12([y.id[0]] + [zero] * 5 + [y.id[1]] + [zero] * 5)
        return cls((nx / w **2, ny / w**3))

    def linefunc(self):
        # https://github.com/ethereum/research/blob/9a7b6825b0dee7a59a03f8ca1d1ec3ae7fb6d598/zksnark/bn128_pairing.py
        pass



ECGBN128.G1 = ECGBN128(
    BN128FP(const.BN128_G1x),
    BN128FP(const.BN128_G1y)
)

ECGBN128.G2 = ECGBN128(
    BN128FP2(const.BN128_G2x),
    BN128FP2(const.BN128_G2y)
)

ECGBN128.G = ECGBN128.G1

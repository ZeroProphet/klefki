"""
ref: https://github.com/ethereum/research/blob/711bd9532b4534ef5ae6277bd7afe625195506d5/zksnark/bn128_field_elements.py
"""
import abc
import zkp_playground.const as const
from zkp_playground.algebra.fields import FiniteField
from zkp_playground.algebra.fields import PolyExtField
from zkp_playground.algebra.groups.ecg import PairFriendlyEllipticCurveGroup
from zkp_playground.curves.arith import short_weierstrass_form_curve_addition


class BLS12_381FP(FiniteField):
    P = const.BLS12_381_P


class BLS12_381FP2(PolyExtField):
    DEG = 2
    F = BLS12_381FP
    P = [BLS12_381FP(e) for e in const.BLS12_381_FP2_E]

    @classmethod
    def from_BLS12_381FP(cls, v):
        return [v, cls.F.zero()]


class BLS12_381FP12(PolyExtField):
    DEG = 12
    F = BLS12_381FP
    P = [BLS12_381FP(e) for e in const.BLS12_381_FP12_E]

    @classmethod
    def from_BLS12_381FP(cls, v):
        return [v] + ([cls.F.zero()] * 11)

    @classmethod
    def from_BLS12_381FP2(cls, v):
        zero = cls.F.zero()
        return [v.id[0]] + [zero] * 5 + [v.id[1]] + [zero] * 5


class BLS12_381ScalarFP(FiniteField):
    P = const.BLS12_381_N


# TODO: sets and caching by memoize() decorator do not work without hashing
# It just a hack now and it should be rechecked
class BLS12_381ScalarHashableFP(BLS12_381ScalarFP):
    def __hash__(self):
        return self.id

    @property
    def n(self):
        return self.value


class ECGBLS12_381(PairFriendlyEllipticCurveGroup):
    """
    y**2 = x**3 + 4
    """
    A = const.BLS12_381_A
    N = const.BLS12_381_N
    F = BLS12_381ScalarFP

    def op(self, g):
        if g == self.zero():
            return self
        if self == self.zero():
            return g
        field = self.id[0].type

        # a1,a3,a2,a4,a6 = 0, 0, 0, a, b
        x, y = short_weierstrass_form_curve_addition(
            self.x, self.y,
            g.x, g.y,
            field.zero(),
            field.zero(),
            field.zero(),
            field(self.A),
            self.B(type(self.x)),
            field
        )
        if x == y == field.zero():
            return self.zero()
        return self.__class__((x, y))

    def twist(self):
        x, y = self.x, self.y
        if self == self.zero():
            return self.zero()
        if isinstance(x, BLS12_381FP12) and isinstance(y, BLS12_381FP12):
            return self
        elif isinstance(x, BLS12_381FP2) and isinstance(y, BLS12_381FP2):
            return self.twist_FP2_to_FP12(x, y)
        elif isinstance(x, BLS12_381FP) and isinstance(y, BLS12_381FP):
            return self.twist_FP_to_FP12(x, y)
        else:
            raise Exception("cannot twist curve to fp12")

    @classmethod
    def twist_FP_to_FP12(cls, x, y):
        # Field isomorphism from Z[p] / x**2 to Z[p] / x**2 - 2*x + 2
        ret = cls(BLS12_381FP12(x), BLS12_381FP12(y))
        assert ret.is_on_curve()
        return ret

    @classmethod
    def twist_FP2_to_FP12(cls, x, y):
        # "Twist" a point in E(FQ2) into a point in E(FQ12)
        zero = BLS12_381FP.zero()
        one = BLS12_381FP.one()
        # https://crypto.stackexchange.com/questions/14669/sextic-twist-optimization-of-bn-pairing-cubic-root-extraction-required/14680#14680
        # "define" the sextic root of 𝜉 as w
        # w=0x^5+0X^4+0X^3+0X^2+1X^1+0X^0).
        w = BLS12_381FP12([zero, one] + [zero] * 10)
        _x = BLS12_381FP2([x.id[0] - x.id[1], x.id[1]])
        _y = BLS12_381FP2([y.id[0] - y.id[1], y.id[1]])
        nx = BLS12_381FP12(_x) / w ** 2
        ny = BLS12_381FP12(_y) / w ** 3
        ret = cls(nx, ny)
        assert ret.is_on_curve()
        return ret

    @staticmethod
    def linefunc(P1, P2, T):

        # https://github.com/ethereum/research/blob/9a7b6825b0dee7a59a03f8ca1d1ec3ae7fb6d598/zksnark/bn128_curve.py
        assert P1 and P2 and T  # No points-at-infinity allowed, sorry
        x1, y1 = P1.x, P1.y
        x2, y2 = P2.x, P2.y
        xt, yt = T.x, T.y
        if x1 != x2:
            m = (y2 - y1) / (x2 - x1)
            return m * (xt - x1) - (yt - y1)
        elif y1 == y2:
            m = (x1**2 * 3) / (y1 * 2)
            return m * (xt - x1) - (yt - y1)
        else:
            return xt - x1

    @classmethod
    def miller_loop(cls, Q, P):
        # https://crypto.stanford.edu/pbc/notes/ep/miller.html
        # ref: https://github.com/ethereum/research/blob/9a7b6825b0dee7a59a03f8ca1d1ec3ae7fb6d598/zksnark/bn128_pairing.py
        log_ate_loop_count = 62
        ate_loop_count = 15132376222941642752

        if Q == cls.zero() or P == cls.zero():
            return cls.one()

        R = Q
        f = BLS12_381FP12.one()

        for i in range(log_ate_loop_count, -1, -1):
            f = f * f * cls.linefunc(R, R, P)
            R = R @ 2
            if ate_loop_count & (2**i):
                f = f * cls.linefunc(R, Q, P)
                R = R + Q
        # Q1 = cls(Q.x ** BLS12_381FP.P, Q.y ** BLS12_381FP.P)
        # nQ2 = cls(Q1.x ** BLS12_381FP.P, (-Q1.y) ** BLS12_381FP.P)
        # f = f * cls.linefunc(R, Q1, P)
        # R = R + Q1
        # f = f * cls.linefunc(R, nQ2, P)
#        R = R + nQ2
        return f ** ((BLS12_381FP.P ** 12 - 1) // cls.N)

    @classmethod
    def pairing(cls, P, Q):
        """
        e(P, Q + R) = e(P, Qj * e(P, R)
        e(P + Q, R) = e(P, R) * e(Q, R)
        """
        assert isinstance(Q.x, BLS12_381FP2)
        assert isinstance(P.x, BLS12_381FP)
        return cls.miller_loop(Q.twist(), P.twist())

    def is_on_curve(self):
        return self.y**2 - self.x**3 == self.B(type(self.x))

    @staticmethod
    def B(F=BLS12_381FP):
        return {
            "BLS12_381FP2": BLS12_381FP2([const.BLS12_381_B, const.BLS12_381_B]),
            "BLS12_381FP12": BLS12_381FP12([const.BLS12_381_B] + [0] * 11),
            "BLS12_381FP": BLS12_381FP(const.BLS12_381_B)
        }[F.__name__]

    @classmethod
    def lift_x(cls, x):
        F = x.type
        y = (x**3 + x*F(cls.A) + F(cls.B(F)))**(1/2)
        return cls((x, y))


ECGBLS12_381.G1 = ECGBLS12_381(
    BLS12_381FP(const.BLS12_381_G1x),
    BLS12_381FP(const.BLS12_381_G1y)
)

ECGBLS12_381.G2 = ECGBLS12_381(
    BLS12_381FP2(const.BLS12_381_G2x),
    BLS12_381FP2(const.BLS12_381_G2y)
)

ECGBLS12_381.G = ECGBLS12_381.G1

from klefki.algebra.abstract import Ring
from operator import add, mul
from operator import neg
from itertools import starmap
from functools import partial

__all__ = ["PolyRing"]


def _multiply_polys(a, b):
    o = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            o[i + j] += a[i] * b[j]
    return o


def _add_polys(a, b):
    o = [0] * max(len(a), len(b))
    for i in range(len(a)):
        o[i] += a[i]
    for i in range(len(b)):
        o[i] += b[i]
    return o


def _neg_poly(a):
    return [-x for x in a]


def _div_polys(a, b):
    o = [0] * (len(a) - len(b) + 1)
    remainder = a
    while len(remainder) >= len(b):
        leading_fac = remainder[-1] / b[-1]
        pos = len(remainder) - len(b)
        o[pos] = leading_fac
        remainder = _add_polys(
            remainder,
            _neg_poly(
                _multiply_polys(
                    b,
                    [0] * pos + [leading_fac]
                )
            )
        )[:-1]
    return o


# Make a polynomial which is zero at {1, 2 ... total_pts}, except
# for `point_loc` where the value is `height`
def mk_singleton(point_loc, total_pts, height):
    fac = 1
    for i in range(1, total_pts + 1):
        if i != point_loc:
            fac *= point_loc - i
    o = [height * 1.0 // fac]
    for i in range(1, total_pts + 1):
        if i != point_loc:
            o = multiply_polys(o, [-i, 1])
    return o


class PolyRing(Ring):
    @property
    def degree(self):
        return len(self.id)

    def op(self, rhs: Ring):
        return self.fmap(_add_polys)(self, rhs)

    def inverse(self):
        return self.fmap(_neg_poly)(self)

    def sec_op(self, rhs: Ring):
        return self.fmap(_multiply_polys)(self, rhs)

    def div(self, rhs: Ring):
        return self.fmap(_div_polys)(self, rhs)

    def __floordiv__(self, rhs: Ring):
        return self.div(rhs)

    @classmethod
    def singleton(cls, point_loc, height, total_pts):
        field = height.__class__
        fac = 1
        for i in range(1, total_pts + 1):
            if i != point_loc:
                fac *= point_loc - i
        o = cls([height / height.__class__(fac)])
        for i in range(1, total_pts + 1):
            if i != point_loc:
                o = cls.lift_fmap(mul)(o.id, [-i, 1])
        return o

    @classmethod
    def lagrange_interp(cls, vec):
        o = cls([])
        for i in range(len(vec)):
            o = o + cls.singleton(i + 1, vec[i], len(vec))
        return o

    def __call__(self, x):
        return sum([self.id[i] * x**i for i in range(self.degree)])

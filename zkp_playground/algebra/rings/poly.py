from zkp_playground.algebra.abstract import Ring, Monoid
from operator import add, mul
from operator import neg
from itertools import starmap
from functools import partial

__all__ = ["PolyRing"]


def deg(p):
    if isinstance(p[0], Monoid):
        zero = p[0].__class__.zero()
    else:
        zero = 0
    # rm tailing zeroo
    d = len(p) - 1
    while getattr(p[d], "id", p[d]) == 0 and d:
        d -= 1
    return d


def lc(p):
    return p[p.degree]


def _euclidean_division(a, b):
    # https://en.wikipedia.org/wiki/Polynomial_greatest_common_divisor#Euclidean_division
    if isinstance(b[0], Monoid):
        zero = b[0].__class__.zero()
    else:
        zero = 0
    dega = deg(a)
    degb = deg(b)
    temp = [x for x in a]
    o = [zero for x in a]
    for i in range(dega - degb, -1, -1):
        o[i] += temp[degb + i] / b[degb]
        for c in range(degb + 1):
            temp[c + i] -= o[c]
    return o[:deg(o)+1]


def _multiply_polys(a, b):
    if isinstance(b[0], Monoid):
        zero = b[0].__class__.zero()
    else:
        zero = 0
    o = [zero] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            o[i + j] += a[i] * b[j]
    return o


def _add_polys(a, b):
    if isinstance(b[0], Monoid):
        zero = b[0].__class__.zero()
    else:
        zero = 0
    o = [zero] * max(len(a), len(b))
    for i in range(len(a)):
        o[i] += a[i]
    for i in range(len(b)):
        o[i] += b[i]
    return o


def _neg_poly(a):
    return [-x for x in a]


def _polynomial_long_division(a, b):
    # https://en.wikipedia.org/wiki/Polynomial_long_division
    if isinstance(a[0], int):
        zero = 0
    else:
        zero = a[0].__class__.zero()
    o = [zero] * (len(a) - len(b) + 1)
    remainder = a
    while len(remainder) >= len(b):
        leading_fac = remainder[-1] / b[-1]
        pos = len(remainder) - len(b)
        o[pos] = leading_fac
        # rem = rem -(b * ([0, 0, 0] + rem[-1]/b[-1]))
        remainder = _add_polys(
            remainder,
            _neg_poly(
                _multiply_polys(
                    b,
                    [zero] * pos + [leading_fac]
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

    def from_list(self, o: list):
        return o

    def from_int(self, o: int):
        if o in [0, 1]:
            return o

    def from_tuple(self, o: tuple):
        return list(o)

    def from_PolyExtField(self, o):
        return o.id

    @property
    def degree(self):
        return deg(self.id)

    def op(self, rhs: Ring):
        if not isinstance(rhs, (self.type)):
            return self.type([i + rhs for i in self.id])
        return self.fmap(_add_polys)(self, rhs)

    def inverse(self):
        return self.fmap(_neg_poly)(self)

    def sec_op(self, rhs: Ring):
        if not isinstance(rhs, (self.type)):
            return self.type([i * rhs for i in self.id])
        return self.fmap(_multiply_polys)(self, rhs)

    def div(self, rhs: Ring):
        return self.fmap(_euclidean_division)(self, rhs)

    def mod(self, rhs: Ring):
        poly = self.id
        for exp in range(len(rhs.id) - 2, -1, -1):
            top = poly.pop()
            for i, c in [(i, c) for i, c in enumerate(rhs) if c]:
                poly[exp + i] -= top * c
        return self.type(poly)

    @classmethod
    def identity(cls):
        return PolyRing([])

    def __floordiv__(self, rhs: Ring):
        return self.div(rhs)

    def __iter__(self):
        return self.id.__iter__()

    def __getitem__(self, i):
        return self.id[i]

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
        return sum([self.id[i] * x**i for i in range(len(self.id))])

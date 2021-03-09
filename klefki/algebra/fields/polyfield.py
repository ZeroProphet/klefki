from abc import abstractproperty
from klefki.algorithms import deg, poly_rounded_div
from klefki.algebra.rings import PolyRing
from klefki.algebra.abstract import Field


class PolyExtField(Field, PolyRing):
    """
    $U \subseteq F$, where F is subfield, P is its module cof
    """
    F = abstractproperty()
    P = abstractproperty()
    DEG = abstractproperty()


    def from_int(self, o):
        if o == 0:
            return self.zero().id
        if o == 1:
            return self.one().id
        else:
            return self.F(o)

    def from_list(self, o):
        assert len(o) == self.DEG
        return [self.F(p) for p in o]

    def from_tuple(self, o):
        assert len(o) == self.DEG
        return [self.F(p) for p in o]

    def from_PolyRing(self, o):
        return o.id

    @classmethod
    def sec_identity(cls):
        return cls([cls.F.one()] + [cls.F.zero()] * (cls.DEG - 1))

    @classmethod
    def identity(cls):
        return cls([cls.F.zero()] * cls.DEG)

    def sec_inverse(self):
        field = self.F
        lm, hm = [self.F.one()] + [self.F.zero()] * \
            self.DEG, [self.F.zero()] * (self.DEG + 1)
        low, high = (
            self.id + [self.F.zero()],
            [self.F(m) for m in self.P] + [field(1)]
        )

        while deg(low):
            r = poly_rounded_div(high, low, field)
            r += [field.zero()] * (self.DEG + 1 - len(r))
            nm = [field(x) for x in hm]
            new = [field(x) for x in high]
            # assert len(lm) == len(hm) == len(low) == len(
            #     high) == len(nm) == len(new) == self.DEG + 1
            # et Euclidean alog.
            for i in range(self.DEG + 1):
                for j in range(self.DEG + 1 - i):
                    nm[i+j] -= lm[i] * r[j]
                    new[i+j] -= low[i] * r[j]
            lm, low, hm, high = nm, new, lm, low

        return self.type([i / field(low[0]) for i in lm[:self.DEG]])

    def sec_op(self, rhs):
        if isinstance(rhs, int):
            rhs = self.F(rhs)
        if isinstance(rhs, self.F):
            return self.__class__([c * rhs for c in self.value])
        else:
            poly = PolyRing(self.id).sec_op(rhs).id
            # mod
            for exp in range(self.DEG - 2, -1, -1):
                # if DEG == 2, exp = 0
                # [DEG-2, ..., 0]
                # From high to low
                top = poly.pop()
                # top is a0
                for i, c in [(i, c) for i, c in enumerate(self.P) if c]:
                    # for fp2:
                    # poly[i] = poly[i] - top * P[i]
                    poly[exp + i] -= top * c
            return self.type(poly)

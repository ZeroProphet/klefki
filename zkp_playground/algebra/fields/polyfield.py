from abc import abstractproperty
from zkp_playground.algebra.rings import PolyRing
from zkp_playground.algebra.abstract import Field


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
        return [self.F(p) for p in o] + [self.F.zero()] * (self.DEG - len(o))

    def from_tuple(self, o):
        return [self.F(p) for p in o] + [self.F.zero()] * (self.DEG - len(o))

    def from_PolyRing(self, o):
        return o.id + [self.F.zero()] * (self.DEG - len(o.id))

    @classmethod
    def sec_identity(cls):
        return cls([cls.F.one()] + [cls.F.zero()] * (cls.DEG - 1))

    @classmethod
    def identity(cls):
        return cls([cls.F.zero()] * cls.DEG)

    def sec_inverse(self):
        # http://www-users.math.umn.edu/~garrett/coding/Overheads/12_polyalg_bounds.pdf
        field = self.F
        lm, hm = (
            [self.F.one()] + self.zero().id,
            [self.F.zero()] + self.zero().id
        )

        low, high = (
            self.id + [self.F.zero()],
            self.P + [self.F.one()]
        )

        while PolyRing(low).degree:
            r = PolyRing(high).div(PolyRing(low)).id
            r += [field.zero()] * (self.DEG + 1 - len(r))
            nm = hm
            new = high
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
        # support scalar multi
        if isinstance(rhs, int):
            rhs = self.F(rhs)
        if isinstance(rhs, self.F):
            return self.__class__([c * rhs for c in self.value])
        else:
            return self.type(
                PolyRing(self.id).sec_op(rhs).mod(PolyRing(self.P))
            )

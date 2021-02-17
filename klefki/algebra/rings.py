from klefki.algebra.abstract import Ring
from operator import add, mul
from operator import neg
from itertools import starmap


class PolyRing(Ring):

    @property
    def degree(self):
        return len(self.id)

    def op(self, rhs: Ring):
        return self.type(list(starmap(add, zip(self.id, rhs.id))))

    def inverse(self):
        return self.type(list(map(neg, self.id)))

    def sec_op(self, rhs: Ring):
        return self.type(list(starmap(mul, zip(self.id, rhs.id))))

    def __truediv__(self, rhs: Ring):
        a = self.id
        b = rhs.id
        cls = self.__class__
        o = [0] * (len(a) - len(b) + 1)
        remainder = a
        f = self.lift_fmap(lambda x, y, z: x - (y * z))
        while len(remainder) >= len(b):
            leading_fac = remainder[-1] // b[-1]
            pos = len(remainder) - len(b)
            o[pos] = leading_fac
            remainder = f(
                remainder,
                b,
                [0] * pos + [leading_fac]
            ).id
            return cls(o)

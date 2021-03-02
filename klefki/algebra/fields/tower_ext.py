from abc import abstractproperty
from klefki.algebra.abstract import Field

__all__ = ["FP2", "FP12"]

class FP2(Field):
    F = abstractproperty()
    QNRI = abstractproperty()

    def craft(self, value):
        if value == 0:
            return self.zero().id
        if value == 1:
            return self.one().id
        if isinstance(value, list):
            assert len(value) == 2
            return [self.F(p) for p in value]
        return self.F(value)

    @property
    def a(self):
        return self.id[0]

    @property
    def b(self):
        return self.id[1]

    def op(self, rhs):
        return self.type([self.a + rhs.a, self.b + rhs.b])

    def sec_op(self, rhs):
        if isinstance(rhs, int):
            return self.type([self.a * rhs, self.b * rhs])
        t1 = self.a * rhs.a
        t2 = self.b * rhs.b
        t3 = rhs.a + rhs.b

        b = self.b + self.a
        b *= t3
        b -= t1
        b -= t2
        a = t1 - t2
        return self.type([a, b])

    def inverse(self):
        return self.type([-self.a, -self.b])

    def sec_inverse(self):
        w = self.type([self.a, -self.b])
        c = self.a * self.a + self.b * self.b
        return self.type([w.a * ~c, w.b * c])

    @classmethod
    def identity(cls):
        return cls([cls.F.zero()] * 2)

    @classmethod
    def sec_identity(cls):
        return cls([cls.F.one(), cls.F.zero()])

    def mulQNR(self):
        return self.type([-self.b, self.a]) + self * (1<<self.QNRI)


class FP12(Field):
    F = abstractproperty()

    def craft(self, value):
        if value == 0:
            return self.zero().id
        if value == 1:
            return self.one().id
        if isinstance(value, list):
            assert len(value) == 3
            return [self.F(p) for p in value]
        return self.F(value)

    @property
    def a(self):
        return self.id[0]

    @property
    def b(self):
        return self.id[1]

    @property
    def c(self):
        return self.id[2]

    def op(self, rhs):
        return self.type([self.a + rhs.a, self.b + rhs.b, self.c + rhs.c])

    def sec_op(self, rhs):
        zero_c = rhs.c == self.F.zero()
        zero_b = rhs.b == self.F.zero()
        Z0 = self.a * rhs.a
        if not zero_b:
            Z2 = self.b * rhs.b
        T0 = self.a + self.b
        T1 = rhs.a + rhs.b
        Z1 = T0 * T1
        Z1 -= Z0
        if not zero_b:
            Z1 -= Z2
        T0 = self.b + self.c
        T1 = rhs.b + rhs.c
        Z3 = T0 * T1
        if not zero_b:
            Z3 -= Z2
        T0 = self.a + self.c
        T1 = rhs.a + rhs.c
        T0 *= T1
        if not zero_b:
            Z2 += T0
        else:
            Z2 = T0
        Z2 -= Z0
        b = Z1
        if not zero_c:
            T0 = self.c * rhs.c
            Z2 -= T0
            Z3 -= T0
            b = b + T0.mulQNR()
        a = Z0 + Z3.mulQNR()
        c = Z2
        return self.type([a, b, c])

    def inverse(self):
        return self.type([-self.a, -self.b, -self.c])

    def sec_inverse(self):
        wa = self.a * self.a - (self.b * self.c).mulQNR()
        wb = (self.c * self.c).mulQNR() - self.a * self.b
        wc = self.b * self.b - self.a * self.c
        f = ((self.b * wc).mulQNR() + self.a *
             wa + (self.c * wb).mulQNR()).inverse()
        return cls.type(wa * f, wb * f, wc * f)

    @classmethod
    def identity(cls):
        return cls([cls.F.zero()] * 3)

    @classmethod
    def sec_identity(cls):
        return cls([cls.F.one(), cls.F.zero(), cls.F.zero()])

from abc import abstractproperty
from .abstract import Group
from .fields import FiniteField
from klefki.numbers import invmod


class EllipticCurveGroup(Group):
    # for y^2 = x^3 + A * x + B
    A = abstractproperty()
    B = abstractproperty()

    def fmap(self, o):
        if isinstance(o, JacobianGroup):
            z = ~(o.value[2])
            return (o.value[0] * z ** 2, o.value[1] * z ** 3)
        return o

    def op(self, g):
        # https://www.desmos.com/calculator/ialhd71we3
        if g.value == 0:
            return self
        if self.value == 0:
            return g

        field = self.value[0].__class__

        if self.value[0] == g.value[0]:
            if self.value[1] == -(g.value[1]):
                return self.identity()
            m = (field(3) * self.value[0] * self.value[0] +
                 field(self.A)) / (field(2) * self.value[1])
        else:
            m = (self.value[1] - g.value[1]) / (self.value[0] - g.value[0])

        r_x = m * m - self.value[0] - g.value[0]
        r_y = self.value[1] + m * (r_x - self.value[0])
        return self.__class__((r_x, -r_y))

    def inverse(self):
        if self.value == 0:
            return self
        return self.__class__((self.value[0], -self.value[1]))

    @classmethod
    def identity(cls):
        # The abstract zero of EC Group
        return cls(0)

    @property
    def x(self):
        if self == self.zero():
            return 0
        return self.value[0]

    @property
    def y(self):
        if self == self.zero():
            return 0
        return self.value[1]

    @classmethod
    def lift_x(cls, x: FiniteField):
        F = x.__class__
#        y = (x**3 + F(cls.A) * x + F(cls.B))**(1/2)
        y = (x**3 + x*F(cls.A) + F(cls.B))**(1/2)
        return cls((x, y))


class CyclicAddGroup(Group):
    # Order of subgroup
    N = abstractproperty()

    def fmap(self, o):
        value = getattr(o, 'value', o)
        return value % self.N

    @classmethod
    def identity(cls):
        return cls(0)

    def inverse(self):
        return self.__class__(invmod(self.value, self.N))

    def op(self, g):
        if isinstance(g, int):
            g = self.type(g)
        return self.__class__(
            (self.value + g.value) % self.N
        )

    def __pow__(self, times):
        return self.__class__(
            pow(self.value, times, self.N)
        )


class EllipicCyclicSubgroup(EllipticCurveGroup):
    '''
    With Lagrange's therem
    the order of a subgroup is a divisor of the order of the parent group
    '''
    # Order of subgroup
    N = abstractproperty()

    def scalar(self, times):
        if hasattr(times, "value"):
            times = times.value
        times = times % self.N
        return super().scalar(times)


class JacobianGroup(Group):
    A = abstractproperty()
    B = abstractproperty()

    def fmap(self, o):
        if isinstance(o, EllipticCurveGroup):
            field = o.value[0].__class__
            return [o.value[0], o.value[1], field(1)]
        return o

    def double(self, n=None):
        if not n:
            n = self
        field = n.value[0].__class__
        if not n.value[1].value:
            return n.__class__(
                (
                    field(0),
                    field(0),
                    field(0)
                )
            )

        ysq = self.value[1] ** 2
        S = self.value[0] @ 4 * ysq
        M = (self.value[0] ** 2) @ 3 + (self.value[2] ** 4) @ self.A
        nx = M ** 2 - S @ 2
        ny = M * (S - nx) - (ysq ** 2) @ 8
        nz = field(2) * self.value[1] * self.value[2]
        return self.__class__((nx, ny, nz))

    @classmethod
    def identity(cls):
        return cls(0)

    def inverse(self):
        pass

    def op(self, g):
        field = self.value[0].__class__
        if not g.value:
            return self
        if not self.value:
            return g
        U1 = self.value[0] * g.value[2] ** 2
        U2 = g.value[0] * self.value[2] ** 2
        S1 = self.value[1] * g.value[2] ** 3
        S2 = g.value[1] * self.value[2] ** 3
        if U1 == U2:
            if S1 != S2:
                return self.__class__(
                    (
                        field(0),
                        field(0),
                        field(1)
                    )
                )
            return self.double()
        H = field(U2.value - U1.value)
        R = field(S2.value - S1.value)
        H2 = H * H
        H3 = H * H2
        U1H2 = U1 * H2
        nx = (R ** 2) - H3 - (U1H2 @ 2)

        ny = R * (U1H2 - nx) - S1 * H3
        nz = H * self.value[2] * g.value[2]
        return self.__class__((nx, ny, nz))

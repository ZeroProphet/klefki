from abc import abstractproperty
from .abstract import Group
from .fields import FiniteField


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

        if self.value[0] != g.value[0]:
            #  m = \frac{y_1 - y_2}{x_1 - x_2}
            m = (self.value[1] - g.value[1]) / (self.value[0] - g.value[0])

        if self.value[0] == g.value[0]:
            if self.value[1] == -(g.value[1]):
                return self.identity

            m = (field(3) * self.value[0] * self.value[0] +
                 field(self.A)) / (field(2) * self.value[1])

        r_x = (m * m - self.value[0] - g.value[0])
        r_y = (self.value[1] + m * (r_x - self.value[0]))
        return self.__class__((r_x, -r_y))

    def inverse(self):
        if self.value == 0:
            return self
        return self.__class__((self.value[0], -self.value[1]))

    @property
    def identity(self):
        # The abstract zero of EC Group
        return self.__class__(0)


class CyclicGroup(Group):
    '''
    With Lagrange's therem
    the order of a subgroup is a divisor of the order of the parent group
    '''
    # The Base Point
    G = abstractproperty()
    # Order of subgroup
    N = abstractproperty()

    def fmap(self, o):
        if isinstance(o, FiniteField):
            return o.__class__(o.value % self.N)
        return getattr(o, 'value', o) % self.N

    def op(self, g):
        '''
        2 + 3 -> 2G + 3G -> 5G
        '''
        if g.value == 0:
            return self
        res = self.value + g.value
        return self.__class__(res % self.N)

    def inverse(self):
        if self.value == 0:
            return self
        return self.__class__(self.N - 1 - self.value)

    @property
    def identity(self):
        return self.__class__(0)


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

    @property
    def identity(self):
        return self.__class__(0)

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

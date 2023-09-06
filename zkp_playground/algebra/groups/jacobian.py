from abc import abstractproperty
from zkp_playground.algebra.abstract import Group
from zkp_playground.algebra.groups.ecg import EllipticCurveGroup


class JacobianGroup(Group):
    A = abstractproperty()
    B = abstractproperty()

    def from_EllipticCurveGroup(self, o):
        field = o.value[0].__class__
        return [o.value[0], o.value[1], field(1)]

    def from_list(self, o):
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

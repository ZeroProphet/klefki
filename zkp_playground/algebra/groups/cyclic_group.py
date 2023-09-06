from zkp_playground.algebra.abstract import Group
from zkp_playground.numbers import invmod
from abc import abstractproperty

__all__ = ["FiniteCycicGroup"]


class FiniteCycicGroup(Group):
    # Order of subgroup
    N = abstractproperty()

    def from_int(self, o):
        return o % self.N

    def from_FiniteField(self, o):
        return o.value % self.N

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

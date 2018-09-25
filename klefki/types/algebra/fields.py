from abc import abstractproperty
from .abstract import Field
from klefki.algorithms import extended_euclidean_algorithm


class FiniteField(Field):

    P = abstractproperty()

    def fmap(self, o):
        return getattr(o, 'value', o) % self.P

    @property
    def identity(self):
        return self.__class__(0 % self.P)

    @property
    def sec_identity(self):
        return self.__class__(1 % self.P)

    def inverse(self):
        return self.__class__(self.P - self.value)

    def mod(self, a, b):
        if isinstance(a, complex):
            return complex((a.real % b), (a.imag % b))
        return a % b

    def sec_inverse(self):
        gcd, x, y = extended_euclidean_algorithm(self.value, self.P)
        assert (self.value * x + self.P * y) == gcd
        if gcd != 1:
            # Either n is 0, or p is not prime number
            raise ValueError(
                '{} has no multiplicate inverse '
                'modulo {}'.format(self.value, self.P)
            )
        return self.__class__(x % self.P)

    def op(self, g):
        return self.__class__(
            self.mod(
                (self.value + g.value), self.P
            )
        )

    def sec_op(self, g):
        return self.__class__(
            self.mod(
                (self.value * g.value), self.P
            )
        )

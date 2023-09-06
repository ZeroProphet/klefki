from abc import abstractproperty
from zkp_playground.algebra.abstract import Field
from zkp_playground.algorithms import extended_euclidean_algorithm
from zkp_playground.algorithms import complex_truediv_algorithm
from zkp_playground.algebra.rings import PolyRing


class PrimeField(Field):

    P = abstractproperty()

    def from_int(self, o):
        return o % self.P

    def from_PrimeField(self, o):
        return o.value % self.P

    def from_complex(self, o):
        return complex((o.real % self.P), (o.imag % self.P))

    def inverse(self):
        return self.__class__(self.P - self.value)

    def mod(self, a, b):
        if isinstance(a, complex):
            return complex((a.real % b), (a.imag % b))
        return a % b

    def sec_inverse(self):
        if isinstance(self.value, complex):
            return complex_truediv_algorithm(complex(1), self.value, self.__class__)

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
        if isinstance(g, int):
            g = self.type(g)
        return self.__class__(
            self.mod(
                (self.value + g.value), self.P
            )
        )

    def sec_op(self, g):
        if isinstance(g, int):
            g = self.type(g)
        return self.__class__(
            self.mod(
                (self.value * g.value), self.P
            )
        )


FiniteField = PrimeField
Fq = FiniteField

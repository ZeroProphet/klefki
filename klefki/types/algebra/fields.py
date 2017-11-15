from abc import abstractproperty
from .abstract import Field
from klefki.algorithms import extended_euclidean_algorithm


class FiniteField(Field):

    P = abstractproperty()

    def fmap(self, v):
        return getattr(v, 'value', v) % self.P

    @property
    def identity(self):
        return self.__class__(0 % self.P)

    @property
    def sec_identity(self):
        return self.__class__(1 % self.P)

    def inverse(self):
        return self.__class__(-self.value % self.P)

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

    def op(self, n):
        return self.__class__((self.value + n.value) % self.P)

    def sec_op(self, n):
        return self.__class__((self.value * n.value) % self.P)

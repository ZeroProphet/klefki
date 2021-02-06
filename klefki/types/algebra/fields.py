from abc import abstractproperty
from .abstract import Field
from klefki.algorithms import extended_euclidean_algorithm
from klefki.algorithms import complex_truediv_algorithm
from klefki.algorithms import deg, poly_rounded_div


class FiniteField(Field):

    P = abstractproperty()

    def fmap(self, o):
        value = getattr(o, 'value', o)
        if isinstance(value, complex):
            return complex((value.real % self.P), (value.imag % self.P))
        return value % self.P

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
        if isinstance(self.value, complex):
            return complex_truediv_algorithm(complex(1), self.value, self.__class__)

        gcd, x, y = extended_euclidean_algorithm(self.value, self.P)
        assert (self.value * x + self.P * y) == gcd
        # if gcd != 1:
        #     # Either n is 0, or p is not prime number
        #     raise ValueError(
        #         '{} has no multiplicate inverse '
        #         'modulo {}'.format(self.value, self.P)
        #     )
        return self.__class__(x % self.P)

    def op(self, g):
        if isinstance(g, int):
            g = self.functor(g)
        return self.__class__(
            self.mod(
                (self.value + g.value), self.P
            )
        )

    def sec_op(self, g):
        if isinstance(g, int):
            g = self.functor(g)
        return self.__class__(
            self.mod(
                (self.value * g.value), self.P
            )
        )


class PolyExtField(Field):
    module_coeffs = abstractproperty()
    degree = abstractproperty()

    def op(self, rhs):
        return self.__class__([x + y for x, y in zip(self.value, rhs.value)])

    def inv(self):
        return self.__class__([-x for x in self.value])

    def sec_op(self, rhs):
        field = self.value[0].__class__
        b = [field(0)] * (self.degree * 2 - 1)
        for i in range(self.degree):
            for j in range(self.degree):
                b[i + j] = b[i + j] + self.value[i] * rhs.value[j]
        while len(b) > self.degree:
            exp, top = len(b) - self.degree - 1, b.pop()
            for i in range(self.degree):
                b[exp + i] = b[exp + 1] - top * field(self.modulus_coeffs[i])
        return self.__class__(b)

    def sec_inverse(self):
        lm, hm = [1] + [0] * self.degree, [0] * (self.degree + 1)
        low, high = self.value + [0], self.modulus_coeffs + [1]
        while deg(low):
            r = poly_rounded_div(high, low)
            r += [0] * (self.degree + 1 - len(r))
            nm = [x for x in hm]
            new = [x for x in high]
            assert len(lm) == len(hm) == len(low) == len(high) == len(nm) == len(new) == self.degree + 1
            for i in range(self.degree + 1):
                for j in range(self.degree + 1 - i):
                    nm[i+j] -= lm[i] * r[j]
                    new[i+j] -= low[i] * r[j]
            lm, low, hm, high = nm, new, lm, low
        return self.__class__(lm[:self.degree]) / low[0]



PrimeField = FiniteField
Fq = FiniteField

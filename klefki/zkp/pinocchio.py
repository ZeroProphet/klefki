"""
Pinocchio protocol by
Parno, Gentry, Howell and Raykova from 2013 (often called PGHR13);
ref: https://eprint.iacr.org/2013/279.pdf
"""
from klefki.zkp.qap import QAP
from typing import Type
from typing import Iterable, Tuple
from klefki.algebra.groups import EllipticCurveGroup
from klefki.algebra.fields import FiniteField


class PGHR13(QAP):
    @property
    def toxic(self):
        return (self.k_a, self.k_b, self.k_c)

    def setup(self, F: Type[Field], G: EllipticCurveGroup):
        self.G = G
        self.t = randfield(F)
        self.k_a = randfield(F)
        self.k_b = randfield(F)
        self.k_c = randfield(F)

    def proof(self,
              c: Field,
              s: Iterable[FiniteField]
              ) -> Tuple[EllipticCurveGroup, ...]:
        return tuple(map(lambda x: x @ self.G, super.proof(c, s)))

    def verify(self, A, B, C, H, Z):
        return G.e(A, B) / G.e(C, self.G) == G.e(H, Z)

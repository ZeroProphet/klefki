"""
Pinocchio protocol by
Parno, Gentry, Howell and Raykova from 2013 (often called PGHR13);
ref: https://eprint.iacr.org/2013/279.pdf
"""
class PGHR13:
    def __init__(self, F, G):
        """
        Setup toxic:  t, k_a, k_b and k_c

        """
        self.G = G
        self.F = F
        self.t = randfield(F)
        self.k_a = randfield(F)
        self.k_b = randfield(F)
        self.k_c = randfield(F)

    @property
    def toxic(self):
        return (self.k_a, self.k_b, self.k_c)

    def setup(self, A, B, C, H, Z):
        self.pi_a = reduce(add, [self.G@a for a in A])
        self.pi_a_ = self.pi_a @ self.k_a

        self.pi_b = reduce(add, [self.G@b for b in B])
        self.pi_b_ = self.pi_b @ self.k_b

        self.pi_c = reduce(add, [self.G@c for c in C])
        self.pi_c_ = self.pi_c @ self.k_c


    @property
    def pi(self):
        return (self.pi_a, self.pi_b, self.pi_c)

    def check(self, H, Z):
        self.pi_h = self.G @ H
        self.pi_z = self.G @ Z
        return G.e(self.pi_a, self.pi_b) / G.e(self.pi_c, self.G) == G.e(self.pi_h, self.pi_z)

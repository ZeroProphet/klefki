from zkp_playground.zkp.commitment import TrapdoorCommitment
from zkp_playground.algebra.abstract import Group, Field
from zkp_playground.algebra.meta import field
from functools import reduce, partial
from typing import Iterator
from operator import add

__all__ = ['commitment', 'vertex_commitment', 'com', 'PedersonCommitment']


def v_multi(g: [Group], a: [Field]) -> [Group]:
    return reduce(lambda x, y: x+y,
                  list(map(lambda a: a[0] @ a[1], zip(g, a))))


def commitment(x: Field, r: Field, H: Group, G: Group) -> Group:
    return (G ^ x) * (H ^ r)


def vertex_commitment(x: [Field], r: Field, H: Group, G: [Group]) -> Group:
    return v_multi(G, x) * H ^ r


def matrix_commitment(x: [[Field]], r: Field, H: Group, G: [Group]) -> Group:
    return vertex_commitment(G, H, reduce(add, x), r)


def com(x, r, H, G) -> Group:
    '''
    Com(x, r) = xG + rH
    '''
    if type(x) in [
            Iterator,
            list
    ]:
        if type(x[0]) in [
            Iterator,
            list
        ]:
            return matrix_commitment(x, r, H, G)
        return vertex_commitment(x, r, H, G)
    return commitment(x, r, H, G)


class PedersonCommitment(TrapdoorCommitment):

    def __init__(self, G, H, x, r):
        '''
        G, H <- ECC
        '''
        self.G = G
        self.H = H
        self.com = partial(com, G=G, H=H)
        self.x = x
        self.r = r
        self.A = self.com(self.x, self.r)

    def commit(self, y, s):
        self.B = self.com(y, s)
        self.c = self.B
        self.y = y
        self.s = s
        return self.c

    def trapdoor(self, new_secret, x):
        '''
        x is trapdoor
        '''
        r_ = self.r - (new_secret - self.x) * ~x
        self.A = self.com(new_secret, r_)

    def challenge(self, e):
        '''
        e is the random callange
        '''
        self.e = e
        self.response = (
            self.y * self.e + self.x,
            self.s * self.e + self.r
        )
        return self.response

    def proof(self, trans=None):
        if not trans:
            trans = self.transcript
        B, e, s = trans
        assert self.com(*s) == self.A * (self.B ** e)
        return True

    @property
    def transcript(self):
        return (self.c, self.e, self.response)

    @property
    def C(self):
        return self.A

    @property
    def D(self):
        return (self.x, self.r)

    @staticmethod
    def verify(H, G, C, D):
        if C == com(*D, H=H, G=G):
            return D[1]

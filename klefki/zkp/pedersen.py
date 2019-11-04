from klefki.zkp.commitment import Commitment
from klefki.types.algebra.abstract import Group, Field
from klefki.types.algebra.meta import field
from functools import reduce, partial
from typing import Iterator
from operator import add

__all__ = ['commitment', 'vertex_commitment', 'com', 'PedersonCommitment']

def v_multi(g: [Group], a: [Field]) -> [Group]:
    return reduce(lambda x,y: x+y,
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


class PedersonCommitment(Commitment):
    def __init__(self, G, H):
        '''
        G, H <- ECC
        '''
        self.G = G
        self.H = H
        self.com = partial(com, G=G,H=H)

    def commit(self, secret, k, r):
        self.x = secret
        self.k = k
        self.r = r
        self.A = self.com(secret, r)
        self.B = self.com(k, r)
        self.c = (self.A, self.B)
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
            self.x * self.e  + self.k,
            self.r * self.e + self.r
        )
        return self.response


    def proof(self):
        (A, B), e, s = self.transcript
        assert self.com(*s) == B * (A ** e)
        return True

    @property
    def transcript(self):
        return (self.c, self.e, self.response)

    @property
    def C(self):
        return self.c

    @property
    def D(self):
        return (self.x, self.r)

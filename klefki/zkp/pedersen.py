from klefki.types.algebra.abstract import Group, Field
from functools import reduce
from typing import Iterator
from operator import add

__all__ = ['commitment', 'vertex_commitment', 'com']

def v_multi(g: [Group], a: [Field]) -> [Group]:
    return reduce(lambda x,y: x+y,
                  list(map(lambda a: a[0] @ a[1], zip(g, a))))


def commitment(G: Group, H: Group, a: Field, b) -> Group:
    return (G ^ a) * (H ^ b)


def vertex_commitment(G: [Group], H, a: [Field], b) -> Group:
    return v_multi(G, a) * H ^ b


def matrix_commitment(G: [Group], H, a: [[Field]], b) -> Group:
    return vertex_commitment(G, H, reduce(add, a), b)

def com(G, H, a, b) -> Group:
    if type(a) in [
            Iterator,
            list
    ]:
        if type(a[0]) in [
            Iterator,
            list
        ]:
            return matrix_commitment(G, H, a, b)
        return vertex_commitment(G, H, a, b)
    return commitment(G, H, a, b)

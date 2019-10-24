from klefki.types.algebra.abstract import Group, Field
from functools import reduce
from typing import Iterator
from operator import add

__all__ = ['commitment', 'vertex_commitment', 'com']

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

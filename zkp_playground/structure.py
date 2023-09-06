from typing import Iterable, Iterator
from math import log2
from itertools import starmap
from hashlib import sha256
from zkp_playground.utils import concat, trunks
from collections import namedtuple

__all__ = ['MerkleTree']


class MerkleLeaf:
    def __init__(self, value, children=None, parent=None):
        self.value = value
        self.children = children or []
        self.parent = parent

    def __repr__(self):
        return "<MerlkeTree::Leaf(%s)>" % self.value


class MerkleTree:
    def __init__(
        self,
        value,
        is_leaf=False,
        parent=None,
        hash_fn=lambda x, y: concat(sha256(x).digest(), sha256(y).digest())
    ):
        self.hash_fn = hash_fn
        self._value = list(value)
        if not len(self.value) % 2 == 0:
            self.value.append(self.value[-1])
        self.leaves = map(MerkleLeaf, self.value)
        self._build_tree(self.leaves)

    def _build_tree(self, leaves):
        height = 0
        while 1:
            leaves_nl = []
            for (l, r) in trunks(leaves, 2):
                leaf = MerkleLeaf(
                    self.hash_fn(l.value, r.value),
                    children=[l, r]
                )
                leaves_nl.append(leaf)
                l.parent = leaf
                r.parent = leaf
            leaves = leaves_nl
            height += 1
            if len(leaves) == 1:
                self._root = leaves[0]
                self._height = height
                break

    @property
    def height(self):
        return self._height

    @property
    def root(self):
        return self._root

    @property
    def value(self):
        return self._value


def get_root(data, hash_fn):
    assert len(data) % 2 == 0
    for i in range(int(log2(len(data)))):
        data = [hash_fn(d[0], d[1]) for d in list(trunks(data, 2))]
    return data


def height(data):
    return int(log2(len(data)))


def path(index, height):
    ret = []
    for i in range(height-1):
        if index % 2 == 0:
            ret.append(index+1)
        else:
            ret.append(index-1)
            index = index - 1
        index = (index // 2)
    return ret

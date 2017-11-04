from typing import Iterable, Iterator
from itertools import starmap
from klefki.utils import dhash256, concat, trunks

__all__ = ['MerkleTree']


class MerkleTree():
    def __init__(self, data: Iterable, child=None) -> None:
        data = list(data)
        if not child and len(data) % 2 != 0:
            data.append(data[-1])
        self.data = data
        self._nodes = None
        self._parents = None

    @property
    def nodes(self) -> Iterator:
        if self._nodes is None:
            self._nodes = list(map(dhash256, self.data))
        return self._nodes

    @property
    def parents(self) -> Iterator:
        if self._parents is None:
            self._parents = self.__class__(
                map(
                    dhash256,
                    list(starmap(
                        concat,
                        trunks(self.nodes, 2)
                    ))
                ),
                child=self
            )
        return self._parents

    @property
    def root(self):
        if len(self.parents.nodes) > 1:
            return self.parents.root
        else:
            return self.parents

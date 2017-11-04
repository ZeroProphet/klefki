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

    @property
    def nodes(self) -> Iterator:
        return map(dhash256, self.data)

    @property
    def parents(self) -> Iterator:
        return self.__class__(
            map(
                dhash256,
                starmap(
                    concat,
                    trunks(self.nodes, 2)
                )
            ),
            child=self
        )

from klefki.types.structure import MerkleTree


def test_mktree():
    l = map(bytes, [1, 2, 3, 4, 5, 6])
    t = MerkleTree(l)
    assert t.parents
    assert len(list(t.parents.nodes)) == 3

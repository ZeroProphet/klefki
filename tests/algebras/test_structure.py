from klefki.structure import MerkleTree


def test_mktree():
    l = map(bytes, [1, 2, 3, 4, 5, 6])
    t = MerkleTree(l)
    assert t.root
    assert t.height == 2

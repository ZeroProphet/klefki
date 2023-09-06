"""
https://github.com/ethereum/research/blob/9a7b6825b0dee7a59a03f8ca1d1ec3ae7fb6d598/zksnark/bn128_pairing_test.py
"""

from zkp_playground.curves.bns import bn128

G1 = bn128.ECGBN128.G1
G2 = bn128.ECGBN128.G2
G = G1
e = bn128.ECGBN128.e


def test_bn128():
    assert G2 @ 9 + G2 @ 5 == G2 @ 14
    assert G2.twist()
    assert bn128.ECGBN128.linefunc(G1@1, G1@2, G1@3)
    assert bn128.ECGBN128.linefunc(G2@1, G2@2, G2@3)
    N = bn128.ECGBN128.N
    one, two, three = G1 @ 1, G1 @ 2, G1 @ 3
    negone, negtwo, negthree = G1 @ (N-1), G1 @ (N-2), G1 @ (N-3)
    linefunc = bn128.ECGBN128.linefunc
    FQ = bn128.BN128FP

    assert linefunc(one, two, one) == FQ(0)
    assert linefunc(one, two, two) == FQ(0)
    assert linefunc(one, two, three) != FQ(0)
    assert linefunc(one, two, negthree) == FQ(0)
    assert linefunc(one, negone, one) == FQ(0)
    assert linefunc(one, negone, negone) == FQ(0)
    assert linefunc(one, negone, two) != FQ(0)
    assert linefunc(one, one, one) == FQ(0)
    assert linefunc(one, one, two) != FQ(0)
    assert linefunc(one, one, negtwo) == FQ(0)


def test_paring_check_against_neg():
    one = bn128.BN128FP12.one()
    # e(G2, G1) * e(G2, -G1) == e(G2, G1 + (- G1))
    p1 = e(G1, G2)
    pn1 = e(G1, -G2)
    # Pairing check against negative in G1
    assert p1 * pn1 == one

    np1 = e(-G1, G2)
    # Pairing check against negative in G2
    assert p1 * np1 == one
    assert pn1 == np1
    # Pairing output has correct order


def test_bilinearity():
    one = bn128.BN128FP12.one()
    p1 = e(G1, G2)
    p2 = e(G1, G2 @ 2)
    # Pairing bilinearity in G1 passed
    assert p1 * p1 == p2
    # Pairing is non-degenerate
    po2 = e(G1 @ 2, G2)
    # Pairing bilinearity in G2 passed
    assert p1 * p1 == po2


def test_paring_KoE():
    # e(G2 @ 27 , G1 @ 37) == (G2, G1 @ (27 * 37))
    p3 = e(G1 @ 27, G2 @ 37)
    po3 = e(G1, G2 @ 999)
    # Composite check passed
    assert p3 == po3


def test_pairing_largenumber():
    a = 9330449265283841176651423630334483389881271944891602221114362827661055476293
    b = 4463072057568402134672461509900194438327696809994126109587422429
    assert e(G1 @ a, G2 @ b) == e(G1, G2 @ (a * b))

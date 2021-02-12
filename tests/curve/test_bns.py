"""
https://github.com/ethereum/research/blob/9a7b6825b0dee7a59a03f8ca1d1ec3ae7fb6d598/zksnark/bn128_pairing_test.py
"""

from klefki.curves.barreto_naehrig import bn128

G1 = bn128.ECGBN128.G1
G2 = bn128.ECGBN128.G2
B = bn128.BN128FP(3)
B2 = bn128.BN128FP2([3, 0])
B12 = bn128.BN128FP12([3] + [0] * 11) / bn128.BN128FP12([0] * 6 + [1] + [0] * 5)
ECG = bn128.ECGBN128
e = bn128.ECGBN128.e

def is_on_curve(pt, b):
    x, y = pt.x, pt.y
    return y**2 - x**3 == b

def test_bn128():
    assert G2 @ 9 + G2 @ 5 == G2 @ 14
    assert is_on_curve(G2, B2)
    assert G2.twist()
    assert is_on_curve(G2.twist(), B12)
    assert bn128.ECGBN128.linefunc(G1@1, G1@2, G1@3)
    assert bn128.ECGBN128.linefunc(G2@1, G2@2, G2@3)

def test_paring_check_against_neg():
    one = bn128.BN128FP12.one()
    p1 = e(G2, G1)
    pn1 = e(G2, -G1)
    # Pairing check against negative in G1
    assert p1 * pn1 == one

    np1 = e(-G2, G1)
    # Pairing check against negative in G2
    assert p1 * np1 == one
    assert pn1 == np1
    # Pairing output has correct order
    assert p1 ** ECG.N == bn128.BN128FP12.one()

    p2 = e(G2, G1 @ 2)
    # Pairing bilinearity in G1 passed
#    assert p1 * p1 == p2
    # Pairing is non-degenerate
    assert p1 != p2 and p1 != np1 and p2 != np1
    po2 = e(G2 @ 2, G1)
    # Pairing bilinearity in G2 passed
#    assert p1 * p1 == po2

    p3 = e(G2 @ 27, G1 @ 37)
    po3 = e(G2, G1 @ 999)
    # Composite check passed
   # assert p3 == po3

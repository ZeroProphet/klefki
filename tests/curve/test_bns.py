from klefki.curves.barreto_naehrig import bn128

G1 = bn128.ECGBN128.G1
G2 = bn128.ECGBN128.G2
B = bn128.BN128FP(3)
B2 = bn128.BN128FP2([3, 0])
B12 = bn128.BN128FP12([3] + [0] * 11) / bn128.BN128FP12([0] * 6 + [1] + [0] * 5)

def is_on_curve(pt, b):
    x, y = pt.x, pt.y
    return y**2 - x**3 == b

def test_bn128():
    assert G2 @ 9 + G2 @ 5 == G2 @ 14
    assert is_on_curve(G2, B2)
    assert G2.twist()
    assert is_on_curve(G2.twist(), B12)

from klefki.curves.barreto_naehrig import bn128

G1 = bn128.ECGBN128.G1
G2 = bn128.ECGBN128.G2
def test_bn128():
    assert G2 @ 9 + G2 @ 5 == G2 @ 14

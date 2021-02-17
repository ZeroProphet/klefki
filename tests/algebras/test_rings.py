from klefki.algebra.rings import PolyRing
from klefki.curves.baby_jubjub import FiniteFieldBabyJubjub as F


def test_poly_neg():
    poly = [1, 2, 3, 4, 5]
    r = PolyRing(poly)
    assert (-r).id == [-1, -2, -3, -4, -5]
    assert (r // r).id == [1]


def test_lagrange_poly():
    vec = [1, 2, 3, 4]
    ret = PolyRing.lagrange_interp(vec)
    assert list(map(int, ret.id)) == [0, 1, 0, 0]


def test_over_field():
    vec = [F(1), F(2), F(3), F(4)]
    r = PolyRing(vec)
    assert (-r).id == [-x for x in vec]
    assert (r // r).id == [F(1)]
    ret = PolyRing.lagrange_interp(vec)
    # y = x
    assert ret == PolyRing([F(0), F(1), F(0), F(0)])

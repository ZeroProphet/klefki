from klefki.algebra.rings import PolyRing


def test_poly_neg():
    poly = [1, 2, 3, 4, 5]
    r = PolyRing(poly)
    assert (-r).id == [-1, -2, -3, -4, -5]
    assert (r / r).id == [1]


def test_lagrange_poly():
    vec = [1, 2, 3, 4]
    ret = PolyRing.lagrange_interp(vec)
    assert ret.id == [28, -35, 15, -2]

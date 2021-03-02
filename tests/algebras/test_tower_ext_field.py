from klefki.algebra.fields.tower_ext import FP2, FP12
from klefki.curves.barreto_naehrig.bn128 import BN128FP as FQ

class TestFP2(FP2):
    F = FQ
    QNRI = 0

class TestFP12(FP12):
    F = TestFP2


def test_field():
    x = TestFP2.one()
    f = TestFP2([1, 2])
    assert x * 4 == x + x + x + x
    assert x / x == x
    assert f + x == TestFP2([2, 2])


def test_fp12():
    x = TestFP2.one()
    f = TestFP2([1, 2])
    fpx = TestFP12([x, x, f])
    assert fpx * TestFP12.zero() == TestFP12.zero()
    assert fpx + TestFP12.zero() == fpx
    assert fpx * TestFP12.one() == fpx

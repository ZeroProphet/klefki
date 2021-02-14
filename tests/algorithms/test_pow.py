from klefki.algorithms import fast_pow as f
from klefki.curves.barreto_naehrig.bn128 import BN128FP12
from random import randint


def test_pow():
    assert f(3, 2, 1) == 8


def test_ext_field():
    x = BN128FP12([randint(0, 10) for i in range(12)])
    assert x ** 0 == x.one()
    assert x ** 1 == x
    assert x ** 2 == x * x
    assert x ** 3 == x * x * x
    assert x ** 4 == x * x * x * x

from klefki.zkp.r1cs import R1CS
from functools import partial


@R1CS.r1cs
def t(x):
    y = x**3
    return y + x + 5


@R1CS.r1cs
def t2(x):
    y = x
    y = x + 2
    y = x**3
    return y + x + 5 + 2


@R1CS.r1cs
def t3(x, y):
    y = x
    y = x + 2
    y = x**3
    return y + x + 5 + 2


@R1CS.r1cs
def t4(x, y):
    for _ in range(10):
        y = x
        y = x + 2
        y = x**3
    return y + x + 5 + 2


A = 10


@R1CS.r1cs(ctx=locals())
def t5(x, y):
    for _ in range(A):
        y = x
        y = x + 2
        y = x**3
    return y + x + 5 + 2


@R1CS.r1cs(ctx=locals())
def t6(x, y):
    for _ in range(10):
        y = t(x)
        y = x
        y = x + 2
        y = x**3
    return y + x + 5 + 2


def test_r1cs():
    s = t.witness(3)
    assert R1CS.verify(s, *t.r1cs)
    assert s[2] == t(3)

    s = t2.witness(3)
    assert s[2] == t2(3)
    assert R1CS.verify(s, *t2.r1cs)

    s = t3.witness(1, 2)
    assert s[3] == t3(1, 2)
    assert R1CS.verify(s, *t3.r1cs)

    s = t4.witness(1, 2)
    assert s[3] == t4(1, 2)
    assert R1CS.verify(s, *t4.r1cs)

    s = t5.witness(1, 2)
    assert s[3] == t5(1, 2)
    assert R1CS.verify(s, *t5.r1cs)

    s = t6.witness(1, 2)
    assert s[3] == t6(1, 2)
    assert R1CS.verify(s, *t6.r1cs)

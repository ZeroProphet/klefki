from klefki.zkp.r1cs import R1CS


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

def test_r1cs():
    s = t.witness(3)
    assert R1CS.verify(s, *t.r1cs)
    assert s[2] == t(3)

    s = t2.witness(3)
    assert s[2] == t2(3)

    s = t3.witness(1, 2)
    assert s[3] == t3(1, 2)

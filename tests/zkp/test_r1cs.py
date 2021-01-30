from klefki.zkp.r1cs import R1CS
from klefki.curves.baby_jubjub import FiniteFieldBabyJubjub as F
from functools import partial

@R1CS.r1cs
def qeval(x):
    y = x**3
    return y + x + 5

def test_r1cs():
    assert qeval.r1cs_with(3) == ([1, 3, 35, 9, 27, 30],
                             [[0, 1, 0, 0, 0, 0],
                              [0, 0, 0, 1, 0, 0],
                              [0, 1, 0, 0, 1, 0],
                              [5, 0, 0, 0, 0, 1]],
                             [[0, 1, 0, 0, 0, 0],
                              [0, 1, 0, 0, 0, 0],
                              [1, 0, 0, 0, 0, 0],
                              [1, 0, 0, 0, 0, 0]],
                             [[0, 0, 0, 1, 0, 0],
                              [0, 0, 0, 0, 1, 0],
                              [0, 0, 0, 0, 0, 1],
                             [0, 0, 1, 0, 0, 0]])

    s, A, B, C = qeval.r1cs_with(3)
    assert R1CS.verify(s, A, B, C)

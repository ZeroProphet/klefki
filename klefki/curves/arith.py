"""
"""
from klefki.types.algebra.fields import FiniteField

def short_weierstrass_form_curve_addition2(
        u1, v1, u2, v2, a1, a3, a2, a4, a6, f: FiniteField
) -> (FiniteField, FiniteField):
    """
    https://core.ac.uk/download/pdf/10898289.pdf
    E_{W,a1a3a2a4a6} = v^2 + a1uv + a3v = u^3 + a2u^2 + a4u + a6
    for k256 curve: v^2 = u^3 + a * u + b
    a1,a3,a2,a4,a6 = 0, 0, 0, a, b
    for baby_jubjub curve: Bv^2 = x^3 + Ax^2 + x
    a1,a3,a2,a4,a6 = 0, 0, a, 1, 0

    """
    if f(u1) == f(0) and f(v1) == f(0): return (u2, v2)
    elif (f(u2) == f(0) and f(v2) == f(0)): return (u1, v1)
    elif u1 == u2:
        if v1 != v2: return (f(0), f(0))
        elif v1*2 + u1 * a1 + a3 == f(0): return (f(0), f(0))
        else:
            lam = ((u1 ** f(2)) * f(3) + u1 * a2 * f(2) - v1 * a1 + a4) / (v1 * f(2) + u1 * a1 + a3)
            u3 = lam ** f(2) + lam * a1 - a2 - u2 * f(2)
            v3 = lam * (u1 - u3) - v1 - a1 * u3 - a3
            return (u3, v3)
    else:
        lam = (v1 - v2) / (u1-u2)
        u3 = lam ** f(2) + a1 * lam - a2 - u1 - u2
        v3 = lam * (u1-u3) - v1 - a1*u3 - a3
        return (u3, v3)


def short_weierstrass_form_curve_addition3(
        x1, y1, z1, x2, y2, z2, a, b
) -> (FiniteField, FiniteField, FiniteField):
    """
    https://eprint.iacr.org/2015/1060.pdf
    """
    # E: Y^2Z = X^3 + zXZ^2 + bZ^3

    b3 =  b *  3 # 0

    t0 = x1 * x2 # 1
    t1 = y1 * y2 # 2
    t2 = z1 * z2 # 3

    t3 = x1 + y1 # 4
    t4 = x2 + y2 # 5
    t3 = t3 * t4 # 6

    t4 = t0 + t1 # 7
    t3 = t3 - t4 # 8
    t4 = x1 + z1 # 9

    t5 = x2 + z2 #10
    t4 = t4 * t5 #11
    t5 = t0 + t2 #12

    t4 = t4 - t5 #13
    t5 = y1 + z1 #14
    x3 = y2 + z2 #15

    t5 = t5 * x3 #16
    x3 = t1 + t2 #17
    t5 = t5 - x3 #18

    z3 = t4 * a  #19
    x3 = b3 * t2 #20
    z3 = x3 + z3 #21

    x3 = t1 - z3 #22
    z3 = t1 + z3 #23
    y3 = x3 * z3 #24

    t1 = t0 + t0 #25
    t1 = t1 + t0 #26
    t2 = a  * t2 #27

    t4 = b3 * t4 #28
    t1 = t1 + t2 #29
    t2 = t0 - t2 #30

    t2 = a  * t2 #31
    t4 = t4 + t2 #32
    t0 = t1 * t4 #33

    y3 = y3 + t0 #34
    t0 = t5 * t4 #35
    x3 = t3 * x3 #36

    x3 = x3 - t0 #37
    t0 = t3 * t1 #38
    z3 = t5 * z3 #39

    z3 = z3 + t0 #40
    return (x3, y3, z3)

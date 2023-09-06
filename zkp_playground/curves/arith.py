"""
"""
from zkp_playground.algebra.fields import FiniteField


def short_weierstrass_form_curve_addition(
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
    if f(u1) == f.zero() and f(v1) == f.zero():
        return (u2, v2)
    elif f(u2) == f.zero() and f(v2) == f.zero():
        return (u1, v1)
    elif u1 == u2:
        if v1 != v2:
            return (f.zero(), f.zero())
        elif v1*2 + u1 * a1 + a3 == f.zero():
            return (f.zero(), f.zero())
        else:
            lam = ((u1 ** 2) * 3 + u1 * a2 * 2 -
                   v1 * a1 + a4) / (v1 * 2 + u1 * a1 + a3)
            u3 = lam ** 2 + lam * a1 - a2 - u2 * 2
            v3 = lam * (u1 - u3) - v1 - a1 * u3 - a3
            return (u3, v3)
    else:
        lam = (v1 - v2) / (u1-u2)
        u3 = lam ** 2 + a1 * lam - a2 - u1 - u2
        v3 = lam * (u1-u3) - v1 - a1 * u3 - a3
        return (u3, v3)


def short_weierstrass_form_curve_twist_addition(u1, v1, u2, v2, a1, a3, a2, a4, a6, f: FiniteField, d):
    # y^2 + a1 uv + a3v = u^3 + (a2 + da1^2) u^2 + a4u + a6 + da3^2
    # ref: https://en.wikipedia.org/wiki/Twists_of_curves
    a2 = a2 + d * (a1 ** 2)
    a6 = a6 + d * (a3 ** 2)
    return short_weierstrass_form_curve_addition(u1, v1, u2, v2, a1, a3, a2, a4, a6, f)

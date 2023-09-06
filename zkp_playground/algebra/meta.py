from zkp_playground.algebra.fields import FiniteField


def field(p, name="FiniteField"):
    return type(name, (FiniteField, ), {"P": p})


finite_field = field

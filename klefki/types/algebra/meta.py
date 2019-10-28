from .fields import FiniteField

def field(p, name="FiniteField"):
    return type(name, (FiniteField, ), {"P": p})

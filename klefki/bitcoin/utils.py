import base58
from klefki.types.algebra.isomorphism import bijection

__all__ = ['b58encode']

b58encode = bijection(base58.b58decode)(base58.b58encode)

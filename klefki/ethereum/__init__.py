from klefki.crypto.ecdsa.secp256k1 import random_privkey
from .public import gen_pub_key
from .private import encode_privkey
from .address import gen_address_from_priv

__all__ = ['gen_address_from_priv']


def gen_key_pair():
    key = random_privkey()
    return encode_privkey(key), gen_pub_key(key)

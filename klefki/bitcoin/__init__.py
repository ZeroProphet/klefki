from klefki.crypto.ecdsa import random_privkey
from .public import gen_pub_key
from .private import encode_privkey


def gen_key_pair():
    key = random_privkey()
    return encode_privkey(key), gen_pub_key(key)

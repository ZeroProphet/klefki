import sys
import re
from klefki.crypto.ecdsa import random_privkey
from klefki.client.shell import command, router
from klefki import eos, ethereum, bitcoin


def encode_privkey(priv, type):
    return {
        'EOS': eos.private.encode_privkey,
        'BTC': bitcoin.private.encode_privkey,
        'ETH': ethereum.private.encode_privkey
    }[type.upper()](priv)


@command
def wonder(type, pattern):
    pattern = re.compile(pattern)
    try:
        while 1:
            priv = encode_privkey(random_privkey(), type)
            if pattern.match(priv):
                print('Found: %s' % priv)
    except KeyboardInterrupt:
        print('Quit')


if __name__ == "__main__":
    router(sys.argv[1:])

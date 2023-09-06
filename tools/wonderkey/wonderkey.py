import sys
import re
from zkp_playground.crypto.ecdsa.secp256k1 import random_privkey
from zkp_playground.client.shell import command, router
from zkp_playground import eos, ethereum, bitcoin


def encode_privkey(priv, type):
    return {
        'EOS': eos.private.encode_privkey,
        'BTC': bitcoin.private.encode_privkey,
        'ETH': ethereum.private.encode_privkey
    }[type.upper()](priv)


def priv_to_addr(priv, target):
    return {
        'BTC': bitcoin.address.gen_address_from_priv,
        'ETH': ethereum.address.gen_address_from_priv,
        'EOS': eos.address.gen_address_from_priv
    }[target.upper()](priv)


def priv_to_pub(priv, target):
    '''
    Transform your `private` key of `type` to `public` key of `target`
    '''
    return {
        'BTC': bitcoin.public.gen_pub_key,
        'ETH': ethereum.public.gen_pub_key,
        'EOS': eos.public.gen_pub_key
    }[target.upper()](priv)


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


@command
def wonder_pub(type, pattern):
    pattern = re.compile(pattern)
    try:
        while 1:
            priv = random_privkey()
            priv_str = encode_privkey(priv, type)
            pub = priv_to_pub(priv, type)
            if pattern.match(pub):
                print('Found: %s with private key %s' % (pub, priv_str))
    except KeyboardInterrupt:
        print('Quit')


@command
def wonder_address(type, pattern):
    pattern = re.compile(pattern)
    try:
        while 1:
            priv = random_privkey()
            priv_str = encode_privkey(priv, type)
            pub = priv_to_addr(priv, type)
            if pattern.match(pub):
                print('Found: %s with private key %s' % (pub, priv_str))
    except KeyboardInterrupt:
        print('Quit')


if __name__ == "__main__":
    router(sys.argv[1:])

import sys
from klefki.client.shell import command, router
from klefki import eos, ethereum, bitcoin


def decode_privkey(priv, type):
    return {
        'EOS': eos.private.decode_privkey,
        'BTC': bitcoin.private.decode_privkey,
        'ETH': ethereum.private.decode_privkey
    }[type](priv)


@command
def priv_transfer(priv, type, target):
    return {
        'EOS': eos.private.encode_privkey,
        'BTC': bitcoin.private.encode_privkey,
        'ETH': ethereum.private.encode_privkey
    }[target](decode_privkey(priv, type))


@command
def priv_to_address(priv, type, target):
    return {
        'BTC': bitcoin.address.gen_address_from_priv(priv),
        'ETH': ethereum.address.gen_address_from_priv(priv)
    }[target](decode_privkey(priv, type))


@command
def priv_to_pub(priv, type, target):
    return {
        'BTC': bitcoin.public.gen_pub_key,
        'ETH': ethereum.public.gen_pub_key,
        'EOS': eos.public.gen_pub_key
    }[target](decode_privkey(priv, type))


if __name__ == "__main__":
    router(sys.argv[1:])

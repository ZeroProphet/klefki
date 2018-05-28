import sys
from klefki.client.shell import command, router, output
from klefki import eos, ethereum, bitcoin


def decode_privkey(priv, type):
    return {
        'EOS': eos.private.decode_privkey,
        'BTC': bitcoin.private.decode_privkey,
        'ETH': ethereum.private.decode_privkey
    }[type.upper()](priv)


@command
@output
def priv_transfer(priv, type, target):
    return {
        'EOS': eos.private.encode_privkey,
        'BTC': bitcoin.private.encode_privkey,
        'ETH': ethereum.private.encode_privkey
    }[target.upper()](decode_privkey(priv, type))


@command
@output
def priv_to_pub(priv, type, target):
    return {
        'BTC': bitcoin.public.gen_pub_key,
        'ETH': ethereum.public.gen_pub_key,
        'EOS': eos.public.gen_pub_key
    }[target.upper()](decode_privkey(priv, type))


if __name__ == "__main__":
    router(sys.argv[1:])

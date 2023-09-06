import sys
from zkp_playground.client.shell import command, router, output
from zkp_playground import eos, ethereum, bitcoin


def decode_privkey(priv, type):
    return {
        'EOS': eos.private.decode_privkey,
        'BTC': bitcoin.private.decode_privkey,
        'ETH': ethereum.private.decode_privkey
    }[type.upper()](priv)


@command
@output
def priv_transfer(priv, type, target):
    '''
    Transform your `private` key of `type` to `private` key of `target`
    '''
    return {
        'EOS': eos.private.encode_privkey,
        'BTC': bitcoin.private.encode_privkey,
        'ETH': ethereum.private.encode_privkey
    }[target.upper()](decode_privkey(priv, type))


@command
@output
def priv_to_pub(priv, type, target):
    '''
    Transform your `private` key of `type` to `public` key of `target`
    '''
    return {
        'BTC': bitcoin.public.gen_pub_key,
        'ETH': ethereum.public.gen_pub_key,
        'EOS': eos.public.gen_pub_key
    }[target.upper()](decode_privkey(priv, type))


if __name__ == "__main__":
    router(sys.argv[1:])

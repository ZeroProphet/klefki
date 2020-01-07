from functools import reduce
from operator import add
from .consts import OPS
from klefki.bitcoin.sign import sign_bytes


def pay_to_pubhash(privkey, pubkey, address):
    scriptPubKey = reduce(add, [
        OPS.OP_DUP,
        OPS.OP_HASH160,
        address,
        OPS.OP_EQUALVERIFY,
        OPS.OP_CHECKSIG
    ])
    scriptSig = sign_bytes(privkey, scriptPubKey) + pubkey
    return scriptPubKey, scriptSig


def pay_to_scripthash(scripthash):
    return reduce(add, [
    ])

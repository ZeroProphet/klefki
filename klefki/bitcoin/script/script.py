from .consts import OPS


def gen_standard_transation(pubkeyhash):
    return sum([
        OPS.OP_DUP,
        OPS.OP_HASH160,
        pubkeyhash,
        OPS.OP_EQUALVERIFY,
        OPS.OP_CHECKSIG
    ])

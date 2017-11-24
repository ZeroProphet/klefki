from .import consts as C


def gen_script(ops: list) -> bytes:
    def to_bytes(a):
        if type(a) is not bytes:
            return bytes([a])
    return sum(map(to_bytes, ops))


def gen_standard_transation(pubkeyhash):
    return gen_script([
        C.OP_DUP,
        C.OP_HASH160,
        pubkeyhash,
        C.OP_EQUALVERIFY,
        C.OP_CHECKSIG
    ])

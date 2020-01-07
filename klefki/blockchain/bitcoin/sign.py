from typing import Callable
from pyasn1.codec.der.encoder import encode as edr_encode
from pyasn1.codec.der.decoder import decode as edr_decode
import klefki.crypto.ecdsa.secp256k1 as ecdsa
from klefki.asn import signature as sig_asn
from klefki.bitcoin.private import decode_privkey
from klefki.bitcoin.public import decode_pubkey
from klefki.utils import int_to_byte, byte_to_int, b64encode, b58encode
from klefki.types.algebra.concrete import FiniteFieldCyclicSecp256k1 as CF
from klefki.types.algebra.isomorphism import bijection, do


@bijection(edr_encode)
def decode_edr(value):
    return edr_decode(value, asn1Spec=sig_asn.ECDSA_Sig_Value())[0]


sig_encode = do(edr_encode, b58encode)
sig_decode = ~sig_encode


def to_sigtype(sig):
    return tuple([v.value for v in sig])


@bijection(to_sigtype)
def from_sigtype(sig):
    return tuple([CF(v) for v in sig])


def msgsig_to_bytes(v, r, s):
    return chr(v), int_to_byte(r), int_to_byte(s)


@bijection(msgsig_to_bytes)
def msgid_from_bytes(v, r, s):
    return ord(v), byte_to_int(r), byte_to_int(s)


def compose(v, r, s) -> bytes:
    return v + '\x00' * (32 - len(r)) + r + '\X00' * (32 - len(s)) + s


@bijection(compose)
def decompose(b: bytes) -> ecdsa.SigType:
    return b[0], b[1: 33], b[33:]


msgsig_encode: Callable[[ecdsa.SigType], bytes] = do(
    from_sigtype,
    msgsig_to_bytes,
    compose,
    b64encode
)
msgsig_decode: Callable[[bytes], ecdsa.SigType] = ~(msgsig_encode)


def sign(privkey: str, msg: str):
    struct = sig_asn.ECDSA_Sig_Value()
    key = decode_privkey(privkey)
    sig = ecdsa.sign(key, msg)
    struct['r'], struct['s'] = sig[1].value, sig[2].value
    return sig_encode(struct)


def sign_bytes(privkey: str, msg: bytes):
    return sign(privkey, msg.decode())


def verify(pubkey: str, sig: str, msg: str):
    pubkey = decode_pubkey(pubkey)
    sig = sig_decode(sig)
    sig = CF(sig[0]._value), CF(sig[1]._value)
    return ecdsa.verify(pubkey, sig, msg)

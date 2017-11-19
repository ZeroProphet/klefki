import base58
from pyasn1.codec.der.encoder import encode
from pyasn1.codec.der.decoder import decode
from klefki.crypto.ecsda import sign, verify
from klefki.asn import signature as sig_asn
from klefki.bitcoin.address import decode_privkey, decode_pubkey
from klefki.types.algebra.concrete import FiniteFieldCyclicBTC as FC


def sign_with_privkey(privkey: str, msg: str):
    struct = sig_asn.ECDSA_Sig_Value()
    key = decode_privkey(privkey)
    sig = sign(key, msg)
    struct['r'], struct['s'] = sig[0].value, sig[1].value
    return base58.b58encode(encode(struct))


def verify_with_pubkey(pubkey: str, sig: str, msg: str):
    pubkey = decode_pubkey(pubkey)
    sig = base58.b58decode(sig)
    sig, _ = decode(
        sig, asn1Spec=sig_asn.ECDSA_Sig_Value()
    )
    sig = FC(sig[0]._value), FC(sig[1]._value)
    return verify(pubkey, sig, msg)

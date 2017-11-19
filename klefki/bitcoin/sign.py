import base58
from pyasn1.codec.der.encoder import encode
from klefki.crypto.ecsda import sign, verify
from klefki.asn import signature as sig
from klefki.bitcoin.address import decode_privkey


def sign_with_privkey(privkey, msg):
    res = sig.ECDSA_Sig_Value()
    key = decode_privkey(privkey)
    res['r'], res['s'] = sign(key, msg)
    return base58.b58encode(encode(res))


def verify_with_pubkey(pubkey, sig, msg):
    sig, _ = base58.b58decode(sig, asn1Spec=sig.ECDSA_Sig_Value())
    sig = sig[0]._value, sig[1]._value
    return verify(pubkey, sig, msg)

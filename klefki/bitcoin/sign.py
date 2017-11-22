import base58
from pyasn1.codec.der.encoder import encode
from pyasn1.codec.der.decoder import decode
import klefki.crypto.ecsda as ecdsa
from klefki.asn import signature as sig_asn
from klefki.bitcoin.private import decode_privkey
from klefki.bitcoin.public import decode_pubkey
from klefki.types.algebra.concrete import FiniteFieldCyclicBTC as FC


def sign(privkey: str, msg: str):
    struct = sig_asn.ECDSA_Sig_Value()
    key = decode_privkey(privkey)
    sig = ecdsa.sign(key, msg)
    struct['r'], struct['s'] = sig[0].value, sig[1].value
    return base58.b58encode(encode(struct))


def verify(pubkey: str, sig: str, msg: str):
    pubkey = decode_pubkey(pubkey)
    sig = base58.b58decode(sig)
    sig, _ = decode(
        sig, asn1Spec=sig_asn.ECDSA_Sig_Value()
    )
    sig = FC(sig[0]._value), FC(sig[1]._value)
    return ecdsa.verify(pubkey, sig, msg)

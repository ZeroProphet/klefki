import bitcoin
import hashlib
import klefki.crypto.ecdsa.secp256k1 as ecdsa
from klefki.bitcoin import gen_key_pair
from klefki.bitcoin.sign import sign, verify


def test_sign():
    msg = 'test'
    priv = ecdsa.random_privkey()
    pub = ecdsa.pubkey(priv)
    sig = ecdsa.sign(priv, msg)
    assert ecdsa.verify(pub, sig, msg)
    ecdsa.proof()


def test_recover():
    msg = 'test'
    mhash = hashlib.sha256(msg.encode()).digest()
    priv = ecdsa.random_privkey()
    pub = ecdsa.pubkey(priv)
    sig = ecdsa.sign(priv, msg)
    assert ecdsa.verify(pub, sig, msg)
    res = ecdsa.recover_via_msg(sig, msg)
    vrs = sig[0].value, sig[1].value, sig[2].value
    ans = bitcoin.ecdsa_raw_recover(mhash, vrs)
    assert (pub.value[0].value, pub.value[1].value) == ans
    assert pub == res


def test_sign_btc():
    privkey, pubkey = gen_key_pair()
    sig = sign(privkey, 'test')
    assert verify(pubkey, sig, 'test')

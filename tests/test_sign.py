import klefki.crypto.ecsda as ecdsa
from klefki.bitcoin.address import gen_key_pair
from klefki.bitcoin.sign import sign, verify


def test_sign():
    priv = ecdsa.random_privkey()
    pub = ecdsa.pubkey(priv)
    sig = ecdsa.sign(priv, 'test')
    assert ecdsa.verify(pub, sig, 'test')
    ecdsa.proof()


def test_sign_btc():
    privkey, pubkey = gen_key_pair()
    sig = sign(privkey, 'test')
    assert verify(pubkey, sig, 'test')

from klefki.crypto.ecsda import sign, verify, random_privkey, pubkey, proof
from klefki.bitcoin.address import gen_key_pair
from klefki.bitcoin.sign import sign_with_privkey, verify_with_pubkey


def test_sign():
    priv = random_privkey()
    pub = pubkey(priv)
    sig = sign(priv, 'test')
    assert verify(pub, sig, 'test')
    proof()


def test_sign_btc():
    privkey, pubkey = gen_key_pair()
    sig = sign_with_privkey(privkey, 'test')
    assert verify_with_pubkey(pubkey, sig, 'test')

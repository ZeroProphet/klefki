from klefki.crypto.ecsda import sign, verify, random_privkey, pubkey, proof


def test_sigh():
    priv = random_privkey()
    pub = pubkey(priv)
    sig = sign(priv, 'test')
    assert verify(pub, sig, 'test')
    proof()

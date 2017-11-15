from bitcoin import privtopub, pubkey_to_address
from klefki.crypto.ecsda import pubkey, random_privkey
from klefki.bitcoin.address import gen_key_pair, gen_pub_key, gen_address
from klefki.bitcoin.address import decode_pub


def test_key():
    priv, pub = gen_key_pair()
    assert pub == privtopub(priv)
    priv, pub = gen_key_pair()
    assert pub == privtopub(priv)

    priv, pub = gen_key_pair()
    assert pub == privtopub(priv)

    priv, pub = gen_key_pair()
    assert pub == privtopub(priv)

    priv, pub = gen_key_pair()
    assert pub == privtopub(priv)


def test_addr():
    key = random_privkey()
    pub = gen_pub_key(key)
    addr = gen_address(key)
    assert addr == pubkey_to_address(pub)

    key = random_privkey()
    pub = gen_pub_key(key)
    addr = gen_address(key)
    assert addr == pubkey_to_address(pub)


def test_decode_pub():
    key = random_privkey()
    ans = pubkey(key)
    ret = decode_pub(gen_pub_key(key))
    assert ans == ret

    key = random_privkey()
    ans = pubkey(key)
    ret = decode_pub(gen_pub_key(key))
    assert ans == ret

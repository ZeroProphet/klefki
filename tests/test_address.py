from bitcoin import privtopub, pubkey_to_address
from klefki.address import gen_key_pair, gen_random_number, gen_pub_key, gen_address


def test_key():
    priv, pub = gen_key_pair()
    assert pub == privtopub(priv)


def test_addr():
    key = gen_random_number()
    pub = gen_pub_key(key)
    addr = gen_address(key)
    assert addr == pubkey_to_address(pub)

from bitcoin import privtopub, pubkey_to_address
from klefki.address import gen_key_pair, gen_random_number, gen_pub_key, gen_address, encode_pub
from klefki.address import decode_pub, calcu_pub_key


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
    key = gen_random_number()
    pub = gen_pub_key(key)
    addr = gen_address(key)
    assert addr == pubkey_to_address(pub)

    key = gen_random_number()
    pub = gen_pub_key(key)
    addr = gen_address(key)
    assert addr == pubkey_to_address(pub)


def test_decode_pub():
    key = gen_random_number()
    ans = calcu_pub_key(key)
    ret = decode_pub(gen_pub_key(key))
    assert ans == ret

    key = gen_random_number()
    ans = calcu_pub_key(key)
    ret = decode_pub(gen_pub_key(key))
    assert ans == ret

import bitcoin
import base58
from bitcoin import privtopub, pubkey_to_address
from klefki.crypto.ecdsa.secp256k1 import pubkey, random_privkey
from klefki.bitcoin import gen_key_pair
from klefki.bitcoin.address import gen_address_from_priv
from klefki.bitcoin.public import decode_pubkey, gen_pub_key
from klefki.bitcoin.private import encode_privkey, decode_privkey


def test_priv_encode():
    key = random_privkey()
    encoded = encode_privkey(key)
    ans = bitcoin.encode_privkey(key.value, 'wif_compressed')
    t1 = base58.b58decode(ans)
    t2 = base58.b58decode(encoded)
    assert t1 == t2
    assert encoded == ans


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
    addr = gen_address_from_priv(key)
    assert addr == pubkey_to_address(pub)

    key = random_privkey()
    pub = gen_pub_key(key)
    addr = gen_address_from_priv(key)
    assert addr == pubkey_to_address(pub)


def test_decode_pub():
    key = random_privkey()
    ans = pubkey(key)
    ret = decode_pubkey(gen_pub_key(key))
    assert ans == ret

    key = random_privkey()
    ans = pubkey(key)
    ret = decode_pubkey(gen_pub_key(key))
    assert ans == ret


def test_decode_priv():
    key = random_privkey()
    res = decode_privkey(encode_privkey(key))
    assert res == key

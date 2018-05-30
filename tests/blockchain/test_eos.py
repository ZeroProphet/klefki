import base58
from klefki.eos.private import encode_privkey, decode_privkey
from klefki.eos.public import gen_pub_key
from klefki.eos.address import gen_address_from_priv


PUB = 'EOS8PjVopeiNNDxG1Q5McRKPaPtfWFfyXHBfyJwBKJRdp9BjVW7uc'
PUB_1 = 'EOS82LCw7Cedhru3VhXadPXdQmJfB2c3V7afGuCF9D2Vv3w8GCsnf'
PUB_2 = 'EOS7azGNmBbnY9Hwo1w4Mnr1ZtiWY6NUe6X8oZKTxWEHqzvGdv6J6'
PRIV = '5JaRXz8K9FubVjLELwxeYSMvaYj29dnRNUGg1gvH2waX9hC53R4'
PRIV_1 = '5KW7LHzq38CDrFv437C1wyZbErNkT2EvNSen72ngX5x1uoS3zJi'
PRIV_2 = '5J7erQYeBdrHg7aNVciQQh2icKAUZGXfZVHjEe7U78CeNXywUig'

PRIV_3 = "5KYVzK4AxpHmBWWx9QPbXsfZWPdrjTyiRDkdCcTS7i4Af2JTTXK"
PUB_3 = "EOS6zXc83V4sEANrvAEHuF4hVsZC3jZKqXBC43bctyspvumSXTqoZ"
ADDR_3 = "EOS5PsYnLBkkGzRWdHACGQ2V3w6Tmokz3GDz"


def test_priv():
    for p in [PRIV, PRIV_1, PRIV_2]:
        decoded = decode_privkey(p)
        encoded = encode_privkey(decoded)
        assert p == encoded


def test_pub():
    for (_priv, _pub) in zip([PRIV, PRIV_1, PRIV_2], [PUB, PUB_1, PUB_2]):
        decoded = decode_privkey(_priv)
        pub = gen_pub_key(decoded)
        raw_pub = base58.b58decode(_pub[3:]).hex()
        raw_PUB = base58.b58decode(_pub[3:]).hex()
        assert raw_PUB == raw_pub
        assert _pub == pub


def test_addr():
    decoded = decode_privkey(PRIV_3)
    encoded = encode_privkey(decoded)
    assert PRIV_3 == encoded
    pub = gen_pub_key(decoded)
    assert PUB_3 == pub
    addr = gen_address_from_priv(decoded)
    assert ADDR_3 == addr

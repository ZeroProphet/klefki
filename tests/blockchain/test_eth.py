from klefki.ethereum.private import encode_privkey, decode_privkey
from klefki.ethereum.address import gen_address_from_priv

PRIV = "c87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3"
ADDRESS = "0x627306090abaB3A6e1400e9345bC60c78a8BEf57"


def test_priv():
    decoded = decode_privkey(PRIV)
    encoded = encode_privkey(decoded)
    assert PRIV == encoded


def test_addr():
    addr = gen_address_from_priv(decode_privkey(PRIV))
    assert ADDRESS.lower() == addr.lower()

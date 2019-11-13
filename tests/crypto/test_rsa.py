import pytest

from klefki.crypto import rsa
from klefki.const import SECP256K1_P, SECP256K1_N


def test_rsa_block_encrypt():
    rsa_instance = rsa.RSA(SECP256K1_P, SECP256K1_N)
    encrypted = rsa_instance.encrypt_block(1200)
    assert rsa_instance.decrypt_block(encrypted) == 1200


def test_rsa_string_encrypt():
    rsa_instance = rsa.RSA(SECP256K1_P, SECP256K1_N)
    to_be_encrypted = "hello crypto"
    encrypted = rsa_instance.encrypt_string(to_be_encrypted)
    assert rsa_instance.decrypt_string(encrypted) == to_be_encrypted


@pytest.mark.parametrize(
    "operators, expected",
    (
        ((5, 12), 5),
        ((23, 12), 11),
        ((23, 11), 1),
        ((5, 12), 5),
        ((23 ** 13, 12), 11),
    )
)
def test_should_mod_inverse_works_as_expected(operators, expected):
    assert rsa.mod_inverse(*operators) == expected

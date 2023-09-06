import pytest

from zkp_playground.crypto import rsa
from zkp_playground.const import SECP256K1_P, SECP256K1_N


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


def test_ssh_rsa():
    pubkey = "AAAAB3NzaC1yc2EAAAADAQABAAABAQCZfBT9GmtLWYmn/UuNoX7Oj0kTRK5FPvzkNvdI+ICke2yfgpcpGgGp1iV8AyaFg/j1We3oRNm0CAhoa7GaAdrOwG/zUKcmoaVDS0Jo3ICS2hyAZflAtDMoUPZB1CmsN1Fr2WbUfxPR7tmGXGlZH/Me9kHwrgdMgVsO+iYuZ6YZVRdFC5+ncko8ClQUjBAiiDjL44kxOW1aOFDSRVZ6TjKRWEiDqHp3QkdTOL7qJCNAibK/rHsv3meLFpP0QhV/H4B9Bs3xfextGaNIdj4HizOMWPWwcarVuKMeGF5tnHGFJCa/+doESAJmsEIwnVTn50Ue8/J+ZIB5KhXqHER+atGv"
    sig = "8bda1618bf83c925b348d808a130c8f41e6e476430c9e40ebe952663d184b138b797f3171fc541432174133a3d8dfa3f3ad210dd8b451fd84bb0c04c857cbc8d84ec6efef933389e4d684a70ebdd34c833aedefa29f10457c370c59debd7b440317ecf3fcc8b9561e6facc427d14ab011ad43e24f7090d9556540784e53e9d7d3d66d7d79ebbe3118176c983b99f7aacc2b2a099562b00976336407e96b3c3eb8f478cc5ebd6c905dac9566c97a97b921282033da5092c1528bb90545b22219bf15b34b383a757a47ef09d4fa334f445ba61313d9e2c8ced5fe5a5c3e6d699d7509427624b381ca90114dcf2521f707f9c078f86215ce58a7474ad95d7acda10"
    msg = "test"
    assert rsa.RSA.verify_ssh_rsa_sig(sig, msg, pubkey)

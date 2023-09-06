from zkp_playground.crypto.ssss import SSSS
from zkp_playground.const import SECP256K1_P as P
from zkp_playground.algebra.utils import randfield
from zkp_playground.algebra.meta import field
import random


def test_ssss():
    F = field(P)
    s = SSSS(F)
    k = random.randint(1, 100)
    n = k * 3
    secret = randfield(F)

    s.setup(secret, k, n)

    assert s.decrypt([s.join() for _ in range(k-1)]) != secret
    assert s.decrypt([s.join() for _ in range(k+1)]) == secret
    assert s.decrypt([s.join() for _ in range(k+2)]) == secret

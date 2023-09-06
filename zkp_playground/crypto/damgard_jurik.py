from zkp_playground.numbers import invmod
from zkp_playground.numbers import rsa_lambda, rsa_phi
from zkp_playground.numbers import lcm, length
from zkp_playground.numbers import crt
from zkp_playground.crypto.paillier import Paillier
from zkp_playground.algebra.meta import field
from zkp_playground.numbers.primes import generate_prime
from zkp_playground.algebra.utils import randfield
from functools import lru_cache
from math import factorial, gcd
import damgard_jurik as ts_dj


def damgard_jurik_reduce(a: int, n: int, s=1) -> int:
    """Computes i given a = (1 + n)^i (mod n^(s+1)).
    :param a: The integer a in the above equation.
    :param s: The integer s in the above equation.
    :param n: The integer n in the above equation.
    :return: The integer i in the above equation.
    """
    def L(b: int) -> int:
        assert (b - 1) % n == 0
        return (b - 1) // n

    @lru_cache(int(s))
    def n_pow(p: int) -> int:
        return n ** p

    @lru_cache(int(s))
    def fact(k: int) -> int:
        return factorial(k)

    i = 0
    for j in range(1, s + 1):

        t_1 = L(a % n_pow(j + 1))
        t_2 = i

        for k in range(2, j + 1):
            k = k

            i = i - 1
            t_2 = t_2 * i % n_pow(j)
            t_1 = t_1 - (t_2 * n_pow(k - 1) *
                         invmod(fact(k), n_pow(j))) % n_pow(j)

        i = t_1
    return i


class DJPaillier(Paillier):

    def __init__(self, P, Q, s=1, strict=False):
        '''
        if strict == True:
           use Carmichael Number
        else:
           use Euler Number
        '''
        N = P * Q
#        Lam = lcm(P-1, Q-1)
        G = field(N**s, "G")  # n ** s == n if s = 1
        # multiplicative group
        MG = field(N ** (s+1), "N^{s+1}")  # n ** (s +1 ) == n2 in pailer case
        H = field(N, "H")
        # https://crypto.stackexchange.com/questions/29591/lcm-versus-phi-in-rsa
        if strict:
            LG = field(rsa_lambda(P, Q), "PhiGroup")
        else:
            LG = field(rsa_phi(P, Q), "PhiGroup")

        j = generate_prime(length(P))
        assert gcd(j, N) == 1
        x = randfield(H)
        g = MG((MG(1 + N) ** j) * x)

        d = crt(a_list=[0, 1], n_list=[LG.P, G.P])
        assert d % G.P == 1
        assert d % LG.P == 0

        self.s = s
        self.privkey = d
        self.N = N
        self.G = g
        self.pubkey = (N, g)

    @staticmethod
    def cal_privkey(P, Q, s=1):
        return crt(a_list=[0, 1], n_list=[(P-1) * (Q-1), N ** s])

    @classmethod
    def encrypt(cls, m, pub, s=1, r=None):
        N, G = pub

        if hasattr(m, "value"):
            m = m.value
        if not r:
            r = randfield(G.functor)
        else:
            r = G.functor(r)
        return G**m * r**(N**s)

    @classmethod
    def decrypt(cls, c, priv, pub, s=1):
        N, G = pub
        d = priv
        F = field(N**s, "N^s")
        return F(damgard_jurik_reduce((c ** d).value, N, s)) * ~F(damgard_jurik_reduce((G ** d).value, N, s))

    def E(self, m, pub=None, s=None, r=None):
        if not s:
            s = self.s or 1
        return self.encrypt(m, pub or self.pubkey, s=s, r=r)

    def D(self, c, priv=None, pub=None, s=None):
        if not s:
            s = self.s or 1
        return self.decrypt(c, priv or self.privkey, pub or self.pubkey, s=s)

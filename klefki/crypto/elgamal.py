from klefki.types.algebra.concrete import EllipticCurveCyclicSubgroupSecp256k1 as Curve
from klefki.types.algebra.concrete import FiniteFieldCyclicSecp256k1 as F
from klefki.types.algebra.utils import randfield
from klefki.types.algebra.meta import field


class ElGamal():

    def __init__(self, x, g=Curve.G):
        self.privkey = x
        self.pubkey = g, g ** x


    @classmethod
    def encrypt(cls, m, pub):
        g, h = pub
        y = randfield(field(g.N)).value

        m_ = Curve.lift_x(g.x.functor(m))
        s = h ** y
        c1 = g ** y
        c2 = s * m_
        return (c1, c2)


    @classmethod
    def decrypt(cls, x, c):
        c1, c2 = c
        s = c1 ** x
        m = (c2 - s)
        return m.x.value


    def E(self, m):
        return self.encrypt(m, self.pubkey)


    def D(self, c):
        return self.decrypt(self.privkey, c)

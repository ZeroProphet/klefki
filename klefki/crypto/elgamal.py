from klefki.curves.secp256k1 import EllipticCurveGroupSecp256k1 as Curve
from klefki.algebra.concrete import FiniteFieldCyclicSecp256k1 as F
from klefki.algebra.utils import randfield
from klefki.algebra.meta import field
from klefki.algebra.isomorphism import bijection
from klefki.utils import int_to_byte, byte_to_int


def map_to_curve(m, G=Curve.G, bias=1):
    try:
        sm = str(getattr(m, "value", m))
        im = int(str(bias) + sm)
        if im > G.x.functor.P:
            raise Exception("secret too large")
        return Curve.lift_x(G.x.functor(im))
    except AssertionError:
        return map_to_curve(m, G=G, bias=bias+1)


@bijection(map_to_curve)
def map_from_curve(M):
    return int(str(M.x.value)[1:])


class ElGamal():

    def __init__(self, x, g=Curve.G):
        self.privkey = x
        self.pubkey = g, g ** x

    @classmethod
    def encrypt(cls, m, pub):
        g, h = pub
        y = randfield(field(g.N)).value
        m_ = map_to_curve(m)
        s = h ** y
        c1 = g ** y
        c2 = s * m_
        return (c1, c2)

    @classmethod
    def decrypt(cls, x, c):
        c1, c2 = c
        s = c1 ** x
        m = (c2 - s)
        return map_from_curve(m)

    def E(self, m):
        return self.encrypt(m, self.pubkey)

    def D(self, c):
        return self.decrypt(self.privkey, c)

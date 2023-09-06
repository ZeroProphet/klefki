from zkp_playground.algebra.utils import randfield
from zkp_playground.zkp.sigma import NIZK
from zkp_playground.algebra.concrete import FiniteFieldCyclicSecp256k1 as CF
from zkp_playground.algebra.concrete import EllipticCurveGroupSecp256k1 as Curve
from hashlib import sha256


class NIZKSchnoor(NIZK):
    """
    ref: https://crypto.stanford.edu/cs355/19sp/lec5.pdf
         https://tools.ietf.org/html/rfc8235
    """

    @staticmethod
    def proof(x: CF):
        x = CF(x)
        r = randfield(CF)
        G = Curve.G
        u = G @ r
        h = G @ x
        c = CF(int(sha256(
            str(G.x.value).encode() +
            str(G.y.value).encode() +
            str(h.x.value).encode() +
            str(h.y.value).encode() +
            str(u.x.value).encode() +
            str(u.y.value).encode()
        ).hexdigest(), 16))

        z = r + c * x

        return (u, h, c, z)

    @staticmethod
    def verify(u, h, c, z):
        G = Curve.G
        return (c == CF(int(sha256(
            str(G.x.value).encode() +
            str(G.y.value).encode() +
            str(h.x.value).encode() +
            str(h.y.value).encode() +
            str(u.x.value).encode() +
            str(u.y.value).encode()
        ).hexdigest(), 16))) and (
            G@z == u + h@c
        )

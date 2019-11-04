#
# Ref:
#* I. Damg˚ard, J. Groth. Non-interactive and reusable non-malleable commitment schemes. Proc. of 35 th ACM Symp. on Theory of Computing (STOC’03), pp.426- 437, 2003.
#
#
from klefki.types.algebra.concrete import EllipticCurveCyclicSubgroupSecp256k1 as ECC
from klefki.types.algebra.concrete import EllipticCurveGroupSecp256k1 as Cruve
from klefki.types.algebra.concrete import FiniteFieldCyclicSecp256k1 as CF
from klefki.types.algebra.concrete import FiniteFieldSecp256k1 as F
from klefki.types.algebra.utils import randfield
from klefki.bitcoin.address import gen_address
from klefki.utils import to_sha256int
import hmac
from klefki.bitcoin.public import encode_pubkey
from klefki.utils import int_to_byte
from klefki.zkp.commitment import Commitment, Sigma

G = ECC.G
H = Cruve.lift_x(CF(to_sha256int("hello NIRNCS")))


def keygen(F):
    pk = randfield(F)
    vk = ECC.G ** pk
    h = gen_address
    return (pk, vk, h)


def commitment(m, key, ak):
    pk, vk, h = key
    CF = pk.functor
    c, d = (G ** pk, G ** ak), (pk, ak)
    r2 = to_sha256int(gen_address(c[0] + c[1]))
    a = G ** r2
    z = ak + m * pk
    mac = hmac.new(str(ak.value).encode(), encode_pubkey(a).encode()).hexdigest()

    return {
        'C': (c, a, mac),
        'D': (m, d , z)
    }


def decommitment(c):
    (c, a, mac), (m, d , z) = c['C'], c['D']
    assert G ** z == c[1] + c[0] ** m
    assert G @ to_sha256int(gen_address(c[0]+c[1]))  == a
    assert mac == hmac.new(str(d[1].value).encode(), encode_pubkey(a).encode()).hexdigest()
    return m

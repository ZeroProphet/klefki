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
from klefki.zkp.pedersen import PedersonCommitment

G = ECC.G
H = Cruve.lift_x(CF(to_sha256int("hello NIRNCS")))


def keygen(F):
    pk = randfield(F)
    vk = F(to_sha256int(str(pk.value)))
    h = gen_address
    return (pk, vk, h)




class NMCommitment(Commitment):

    def __init__(self, G, H, key=None):
        if not key:
            key = keygen(CF)
        self.key = key

    def commit(self, m, ak):
        pk, vk, h = self.key
        com = PedersonCommitment(H, G, pk, ak)
        # (𝑐,𝑑)=𝐻𝑆𝑐𝑜𝑚𝑚𝑖𝑡𝑝𝑘(𝑎𝑘)
        c, d = com.C, com.D
        # α=ℎ(𝑐)
        alpha = CF(to_sha256int(gen_address(c)))
        # Now we simulate a proof of knowledge of a signature on 𝛼 with challenge 𝑚
        S = PedersonCommitment(H, G, vk, alpha)
        r1, r2 = randfield(vk.functor), randfield(vk.functor)
        a = S.commit(r1, r2)
        z = S.challenge(m)
        self.S = S
        # Finally, we compute 𝑚𝑎𝑐=𝑀𝐴𝐶𝑎𝑘(𝑎).
        mac = hmac.new(str(ak.value).encode(), encode_pubkey(a).encode()).hexdigest()
        self.c = (c, a, mac)
        self.d = (m, d , z)


    @property
    def C(self):
        return self.c

    @property
    def D(self):
        return self.d


    def open(self):
        c, a, mac = self.c
        m, d, z = self.d
        alpha = CF(to_sha256int(gen_address(c)))
        assert mac == hmac.new(str(d[1].value).encode(), encode_pubkey(a).encode()).hexdigest()
        assert self.S.proof
        return m

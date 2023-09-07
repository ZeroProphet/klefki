zkp-playground
===================

----------------------

### Description

**zkp-playground is a playground for ZKP algorithms.**

The project was created on the basis of the [Klefki](https://zeroprophet.github.io/klefki/) and [Plonk_Py](https://github.com/ETHorHIL/Plonk_Py) libraries.

Klefki [Documentation](https://ryankung.github.io/klefki)

### Requirements:
- python>=3.6

### Installation
```shell
pip3 install zkp_playground

zkp_playground shell
```

### ZKP Examples

* Groth16

```python
from zkp_playground.curves.bns.bn128 import BN128ScalarFP as FP, ECGBN128 as ECG
from zkp_playground.zkp.groth16 import groth16
from zkp_playground.zkp.groth16.r1cs import R1CS
from zkp_playground.zkp.groth16.qap import QAP


@R1CS.r1cs(FP)
def f(x, k, c):
    y = x + c + k
    return y ** 3


g = ECG.G1
h = ECG.G2

qap = QAP(f.A, f.B, f.C)
U, V, W, T = qap.qap
a = f.witness(FP(89), FP(8), FP(8))
H = qap.H(a)
R = groth16.RationalGenerator(
    FP, ECG, ECG, ECG, ECG.e, ECG.G1, ECG.G2, 4, U, V, W, T)

tau, sigma = groth16.setup(R, len(a))
pi = groth16.prov(R, H, tau, sigma, a)
assert groth16.vfy(R, tau, a, pi)
```

* Plonk

```python
from zkp_playground.zkp.plonk.trusted_setup import setup_algo
from zkp_playground.zkp.plonk.prover import prover_algo
from zkp_playground.zkp.plonk.verifier import verifier_algo


def permute_idices(wires: list[str]) -> list[int]:
    # This function takes an array "circuit" of arbitrary values and returns an
    # array with shuffles the indices of "circuit" for repeating values
    size = len(wires)
    permutation = [i + 1 for i in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            if wires[i] == wires[j]:
                permutation[i], permutation[j] = permutation[j], permutation[i]
                break
    return permutation


# Wires
a = ["x", "var1", "var2", "1", "1", "var3", "empty1", "empty2"]
b = ["x", "x", "x", "5", "35", "5", "empty3", "empty4"]
c = ["var1", "var2", "var3", "5", "35", "35", "empty5", "empty6"]

wires = a + b + c

# Gates
add = [1, 1, 0, -1, 0]
mul = [0, 0, 1, -1, 0]
const5 = [0, 1, 0, 0, -5]
public_input = [0, 1, 0, 0, 0]
empty = [0, 0, 0, 0, 0]

gates_matrix = [mul, mul, add, const5, public_input, add, empty, empty]
permutation = permute_idices(wires)

# We can provide public input 35. For that we need to specify the position
# of the gate in L and the value of the public input in p_i
L = [4]
p_i = 35
public_inputs = (L, p_i)

n = len(gates_matrix)
# matrix transpose
gates_matrix = list(zip(*gates_matrix))

# To get the witness, the prover applies his private input x=3 to the
# circuit and writes down the value of every wire.
witness = [
    3, 9, 27, 1, 1, 30, 0, 0,
    3, 3, 3, 5, 35, 5, 0, 0,
    9, 27, 30, 5, 35, 35, 0, 0,
]

# We start with a setup that computes the trusted setup and does some
# precomputation
CRS, Qs, p_i_poly, perm_prep, verifier_prep = setup_algo(
    gates_matrix, permutation, *public_inputs
)

# The prover calculates the proof
proof_SNARK, u = prover_algo(witness, CRS, Qs, p_i_poly, perm_prep)

# Verifier checks if proof checks out
verifier_algo(proof_SNARK, n, p_i_poly, verifier_prep, perm_prep[2])
```



### Elliptic Curve Group Example

* Test pairing

```python
from zkp_playground.curves.bns import bn128

G1 = bn128.ECGBN128.G1
G2 = bn128.ECGBN128.G2
G = G1
e = bn128.ECGBN128.e

one = bn128.BN128FP12.one()
p1 = e(G1, G2)
p2 = e(G1 @ 2, G2)
assert p1 * p1 == p2
```

* Create Custom Groups

```python
import zkp_playground.const as const
from zkp_playground.algebra.fields import FiniteField
from zkp_playground.algebra.groups import EllipticCurveGroup
from zkp_playground.curves.arith import short_weierstrass_form_curve_addition


class FiniteFieldSecp256k1(FiniteField):
    P = const.SECP256K1_P


class FiniteFieldCyclicSecp256k1(FiniteField):
    P = const.SECP256K1_N


class EllipticCurveGroupSecp256k1(EllipticCurveGroup):
    """
    y^2 = x^3 + A * x + B
    """

    N = const.SECP256K1_N
    A = const.SECP256K1_A
    B = const.SECP256K1_B

    def op(self, g):
        field = self.id[0].__class__
        x, y = short_weierstrass_form_curve_addition(
            self.x, self.y,
            g.x, g.y,
            field.zero(),
            field.zero(),
            field.zero(),
            field(self.A),
            field(self.B),
            field
        )
        if x == y == field(0):
            return self.__class__(0)
        return self.__class__((x, y))
```

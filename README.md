Klefki
===================

[![travis](https://api.travis-ci.com/ZeroProphet/klefki.svg)](https://travis-ci.com/github/ZeroProphet/klefki)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/RyanKung/klefki/graphs/commit-activity)
[![PyPI version klefki](https://badge.fury.io/py/klefki.svg)](https://pypi.python.org/pypi/klefki/)
[![PyPI license](https://img.shields.io/pypi/l/klefki.svg)](https://pypi.python.org/pypi/klefki/)
[![PyPI status](https://img.shields.io/pypi/status/klefki.svg)](https://pypi.python.org/pypi/klefki/)
[![Generic badge](https://img.shields.io/badge/Document-passing-blue.svg)](https://zeroprophet.github.io/klefki/)

![klefki](res/707Klefki.png)

----------------------

> Klefki (Japanese: クレッフィ Cleffy) is a dual-type Steel/Fairy Pokémon introduced in Generation VI. It is not known to evolve into or from any other Pokémon.

----------------------

# TL; DR

**Klefki is a playground for researching elliptic curve group based algorithms & applications, such as MPC, HE, ZKP, and Bitcoin/Ethereum. All data types & structures are based on mathematical defination of abstract algebra.**

#### [Check the Document](https://ryankung.github.io/klefki)

#### [Try it!](https://repl.it/@RyanKung/Klefki-Demo)


#### For Installation (require python>=3.6):

```shell
pip3 install klefki

klefki shell
```

Have Fun!!!!

## Elliptic Curve Group Example

* Test pairing

```python
from klefki.curves.barreto_naehrig import bn128

G1 = bn128.ECGBN128.G1
G2 = bn128.ECGBN128.G2
G = G1
e = bn128.ECGBN128.e

one = bn128.BN128FP12.one()
p1 = e(G2, G1)
p2 = e(G2, G1 @ 2)
assert p1 * p1 == p2
```

* Create Custom Groups

```python
import klefki.const as const
from klefki.algebra.fields import FiniteField
from klefki.algebra.groups import EllipticCurveGroup
from klefki.algebra.groups import EllipicCyclicSubgroup
from klefki.curves.arith import short_weierstrass_form_curve_addition2


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
        x, y = short_weierstrass_form_curve_addition2(
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


## ZKP Examples

* Play with r1cs

```python
from klefki.zkp.r1cs import R1CS
from functools import partial



@R1CS.r1cs
def t(x):
    y = x**3
    return y + x + 5


s = t.witness(3)
assert R1CS.verify(s, *t.r1cs)
assert s[2] == t(3)
```


## MPC Examples (SSSS/VSS)

```
from klefki.crypto.ssss import SSSS
from klefki.const import SECP256K1_P as P
from klefki.algebra.utils import randfield
from klefki.algebra.meta import field
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

```


## PubKey/PrivKey Examples

With `AAT(Abstract Algebra Type)` you can easily implement the bitcoin `priv/pub key` and `sign/verify` algorithms like this:

```python

import random
from klefki.utils import to_sha256int
from klefki.algebra.concrete import (
    JacobianGroupSecp256k1 as JG,
    EllipticCurveCyclicSubgroupSecp256k1 as CG,
    EllipticCurveGroupSecp256k1 as ECG,
    FiniteFieldCyclicSecp256k1 as CF
)


N = CG.N
G = CG.G


def random_privkey() -> CF:
    return CF(random.randint(1, N))


def pubkey(priv: CF) -> ECG:
    return ECG(JG(G @ priv))


def sign(priv: CF, m: str) -> tuple:
    k = CF(random.randint(1, N))
    z = CF(to_sha256int(m))
    r = CF((G @ k).value[0])  # From Secp256k1Field to CyclicSecp256k1Field
    s = z / k + priv * r / k
    return r, s



def verify(pub: ECG, sig: tuple, mhash: int):
    r, s = sig
    z = CF(mhash)
    u1 = z / s
    u2 = r / s
    rp = G @ u1 + pub @ u2
    return r == rp.value[0]

```

Even proof the `Sign/Verify` algorithm mathematically.


```python
def proof():
    priv = random_privkey()
    m = 'test'
    k = CF(random_privkey())
    z = CF(to_sha256int(m))
    r = CF((G @ k).value[0])
    s = z / k + priv * r / k

    assert k == z / s + priv * r / s
    assert G @ k == G @ (z / s + priv * r / s)
    assert G @ k == G @ (z / s) + G @ priv @ (r / s)

    pub = G @ priv
    assert pub == pubkey(priv)
    assert G @ k == G @ (z / s) + pub @ (r / s)
    u1 = z / s
    u2 = r / s
    assert G @ k == G @ u1 + pub @ u2


```

Or transform your Bitcoin Private Key to EOS Private/Pub key (or back)

```python
from klefki.bitcoin.private import decode_privkey
from klefki.eos.public import gen_pub_key
from klefki.eos.private import encode_privkey


def test_to_eos(priv):
    key = decode_privkey(priv)
    eos_priv = encode_privkey(key)
    eos_pub = gen_pub_key(key)
    print(eos_priv, eos_pub)

```

Klefki
===================

[![travis](https://travis-ci.org/RyanKung/klefki.svg?branch=master)](https://travis-ci.org/RyanKung/klefki)

![klefki](res/707Klefki.png)

----------------------

> Klefki (Japanese: クレッフィ Cleffy) is a dual-type Steel/Fairy Pokémon introduced in Generation VI. It is not known to evolve into or from any other Pokémon.

----------------------

# TL;DR

**Klefki is a playground for researching elliptic curve group based cryptocoins, such as Bitcoin and Ethereum. All data types & structures are based on mathematical defination of abstract algebra.**

#### [Check the Document](https://ryankung.github.io/klefki)

#### [Try it!](https://repl.it/@RyanKung/Klefki-Demo)


#### For Installation (require python>=3.6):

```shell
pip3 install klefki

klefki shell
```

Have Fun!!!!

## AAT(Abstract Algebra Type)

With `AAT(Abstract Algebra Type)` you can easily implement the bitcoin `priv/pub key` and `sign/verify` algorithms like this:

```python

import random
from klefki.utils import to_sha256int
from klefki.types.algebra.concrete import (
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

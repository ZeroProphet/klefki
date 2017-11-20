Klefki
===================

![klefki](res/707Klefki.png)

----------------------

> Klefki (Japanese: クレッフィ Cleffy) is a dual-type Steel/Fairy Pokémon introduced in Generation VI. It is not known to evolve into or from any other Pokémon.

----------------------

# TL;DR

**Klefki is a playground for researching elliptic curve group based cryptocoins, such as Bitcoin. All data types & structures are based on mathematical defination of abstract algebra.**

With `AAT(Abstract Algebra Type)` you can easily implement the bitcoin `priv/pub key` and `sign/verify` algorithms like this:

```python

import random
from klefki.utils import to_sha256int
from klefki.types.algebra.concrete import (
    JacobianGroupBTC as JG,
    EllipticCurveCyclicSubgroupBTC as CG,
    EllipticCurveGroupBTC as ECG,
    FiniteFieldCyclicBTC as CF
)


N = CG.N
G = CG.G


def random_privkey() -> CF:
    return CF(random.randint(1, N))


def pubkey(priv: CF) -> ECG:
    return ECG(JG(G @ priv))


def sign(priv: CF, m: str) -> tuple:
    k = CF(random_privkey())
    z = CF(to_sha256int(m))
    r = CF((G @ k).value[0])  # From BTCField to CyclicBTCField
    s = z / k + priv * r / k
    return r, s


def verify(pub: ECG, sig: tuple, msg: str):
    mhash = to_sha256int(msg)
    return verify_msghash(pub, sig, mhash)

```

# Docs

[Abstract Algebra Types](https://github.com/RyanKung/klefki/blob/master/docs/Abstract%20Algebra%20Types.ipynb)

[ASN.1](https://github.com/RyanKung/klefki/blob/master/docs/ASN.1.ipynb)

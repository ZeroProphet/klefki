
**zkp-playground is a library for researching elliptic curve group based cryptocoins, such as Bitcoin and Ethereum. All data types & structures are based on mathematical defination of abstract algebra.**


#### For Installation (require python>=3.6):

```shell
pip3 install zkp-playground

zkp-playground shell
```

Have Fun!!!!

## AAT(Abstract Algebra Type)

With `AAT(Abstract Algebra Type)` you can easily implement the bitcoin `priv/pub key` and `sign/verify` algorithms like this:

```python

import random
from zkp_playground.utils import to_sha256int
from zkp_playground.types.algebra.concrete import (
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
from zkp_playground.bitcoin.private import decode_privkey
from zkp_playground.eos.public import gen_pub_key
from zkp_playground.eos.private import encode_privkey


def test_to_eos(priv):
    key = decode_privkey(priv)
    eos_priv = encode_privkey(key)
    eos_pub = gen_pub_key(key)
    print(eos_priv, eos_pub)

```


## Bijection

A morphism f : X → Y in a category is an isomorphism if it admits a two-sided inverse.

You can define your bijection encoder/decoder like this.

```python
from zkp_playground.types.algebra.isomorphism import bijection, do
from zkp_playground.asn import signature as sig
from functools import partial
import base58
from pyasn1.codec.der.encoder import encode
from pyasn1.codec.der.decoder import decode


b58encoder = bijection(base58.b58decode)(base58.b58encode)
asn1encoder = bijection(partial(decode, asn1Spec=sig.ECDSA_Sig_Value()))(encode)

data = sig.ECDSA_Sig_Value()
data['r'] = 123
data['s'] = 234

process = do(asn1encoder, b58encoder)
process(data)
>>> 'cTVygpHoWBNR'

(~process)(process(data))
>>> (ECDSA_Sig_Value().setComponentByPosition(0, Integer(123)).setComponentByPosition(1, Integer(234)),
 b'')

```

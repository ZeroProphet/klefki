"""
doc: https://tools.ietf.org/id/draft-kasamatsu-bncurves-01.html
paper: https://eprint.iacr.org/2010/526.pdf
paper: https://eprint.iacr.org/2005/133.pdf

A BN curve [3] is one of the instantiations of pairing-friendly curves proposed in 2005. A pairing over BN curves constructs optimal Ate pairings.

A BN curve is an elliptic curve E defined over a finite field F_p, where p is more than or equal to 5, such that p and its order r are prime numbers parameterized by

    p = 36u^4 + 36u^3 + 24u^2 + 6u + 1
    r = 36u^4 + 36u^3 + 18u^2 + 6u + 1

for some well chosen integer u. The elliptic curve has an equation of the form E: y^2 = x^3 + b, where b is an element of multiplicative group of order p.

BN curves always have order 6 twists. If w is an element which is neither a square nor a cube in a finite field F_p^2, the twisted curve E' of E is defined over a finite field F_p^2 by the equation E': y^2 = x^3 + b' with b' = b/w or b' = bw.

A pairing e is defined by taking G_1 as a cyclic group composed by rational points on the elliptic curve E, G_2 as a cyclic group composed by rational points on the elliptic curve E', and G_T as a multiplicative group of order p^12.
-----------------

ref: https://github.com/herumi/ate-pairing

The two supported BN curves have the following parameters:

    b = 2 and p = 16798108731015832284940804142231733909889187121439069848933715426072753864723; and
    b = 3 and p = 21888242871839275222246405745257275088696311157297823662689037894645226208583.

As usual,

the cyclic group G1 (aka Ec1) is instantiated as E(Fp)[n] where n := p + 1 - t;
the cyclic group G2 (aka Ec2) is instantiated as the inverse image of E'(Fp^2)[n] under a twisting isomorphism from E' to E; and
the pairing e: G1 x G2 -> Fp12 is the optimal ate pairing.

------------
Note:
Suppose that E/F is a field extension. Then E may be considered as a vector space over F (the field of scalars). The dimension of this vector space is called the degree of the field extension, and it is denoted by [E:F].
"""

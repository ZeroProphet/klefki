"""
doc: https://tools.ietf.org/id/draft-kasamatsu-bncurves-01.html
paper: https://eprint.iacr.org/2005/133.pdf

A BN curve [3] is one of the instantiations of pairing-friendly curves proposed in 2005. A pairing over BN curves constructs optimal Ate pairings.

A BN curve is an elliptic curve E defined over a finite field F_p, where p is more than or equal to 5, such that p and its order r are prime numbers parameterized by

    p = 36u^4 + 36u^3 + 24u^2 + 6u + 1
    r = 36u^4 + 36u^3 + 18u^2 + 6u + 1

for some well chosen integer u. The elliptic curve has an equation of the form E: y^2 = x^3 + b, where b is an element of multiplicative group of order p.

BN curves always have order 6 twists. If w is an element which is neither a square nor a cube in a finite field F_p^2, the twisted curve E' of E is defined over a finite field F_p^2 by the equation E': y^2 = x^3 + b' with b' = b/w or b' = bw.

A pairing e is defined by taking G_1 as a cyclic group composed by rational points on the elliptic curve E, G_2 as a cyclic group composed by rational points on the elliptic curve E', and G_T as a multiplicative group of order p^12.
"""

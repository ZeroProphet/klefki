from .polynomial_evalrep import get_omega
from .polynomial_evalrep import polynomialsEvalRep
from .ssbls12 import Fp, Poly, evaluate_in_exponent, random_fp_seeded


def vanishing_poly(omega, n: int) -> Poly:
    # For the special case of evaluating at all n powers of omega,
    # the vanishing poly has a special form.
    #  t(X) = (X-1)(X-omega)....(X-omega^(n-1)) = X^n - 1
    #  X^n - 1 == (-1) + (0*X^1 + 0*X^2 + 0*X^3 + ...) + (1*X^n)
    return Poly([Fp(-1)] + [Fp(0)] * (n - 1) + [Fp(1)])


def accumulator_factor(n, i, witness, beta, id_domain, perm_domain, gamma):
    # This function is used in round 2
    # i am doing permutation[j-1] below because the list starts at 0 and the
    # paper at 1
    res = Fp(1)
    for j in range(i+1):
        nom_1 =   witness[j]         + beta * id_domain[j]     + gamma
        denom_1 = witness[j]         + beta * perm_domain[j]     + gamma

        nom_2 =   witness[n + j]     + beta * id_domain[n+j]   + gamma
        denom_2 = witness[n + j]     + beta * perm_domain[n+j]   + gamma

        nom_3 =   witness[2 * n + j] + beta * id_domain[2*n+j] + gamma
        denom_3 = witness[2 * n + j] + beta * perm_domain[2*n+j] + gamma
        res *= (nom_1 / denom_1) * (nom_2 / denom_2) * (nom_3 / denom_3)
    return res


def prover_algo(witness, CRS, Qs, p_i_poly, perm_precomp):
    print("Starting the Prover Algorithm")
    n = int(len(witness) / 3)

    id_domain, perm_domain, k, Ss = perm_precomp

    # We need to convert between representations to multiply and divide more
    # efficiently. In round 3 we have to divide a polynomial of degree 4*n+6
    # Not sure if there is a big benefit in keeping the lower order
    # representations or if it makes sense to do everything in the highest
    # order 8*n right away...

    # polys represented with n points
    omega = get_omega(Fp, n)
    ROOTS = [omega ** i for i in range(n)]
    PolyEvalRep = polynomialsEvalRep(Fp, omega, n)
    witness = [Fp(i) for i in witness]
    witness_poly_a = PolyEvalRep(ROOTS, witness[:n])
    witness_poly_b = PolyEvalRep(ROOTS, witness[n:n*2])
    witness_poly_c = PolyEvalRep(ROOTS, witness[2*n:])
    vanishing_pol_coeff = vanishing_poly(omega, n)

    # polys represented with 2*n points
    omega2 = get_omega(Fp, 2 * n)
    PolyEvalRep2 = polynomialsEvalRep(Fp, omega2, 2 * n)
    vanishing_poly_ext = PolyEvalRep2.from_coeffs(vanishing_pol_coeff)
    witness_poly_a_ext = PolyEvalRep2.from_coeffs(witness_poly_a.to_coeffs())
    witness_poly_b_ext = PolyEvalRep2.from_coeffs(witness_poly_b.to_coeffs())
    witness_poly_c_ext = PolyEvalRep2.from_coeffs(witness_poly_c.to_coeffs())

    # polys represented with 8*n points
    omega3 = get_omega(Fp, 8 * n)
    PolyEvalRep3 = polynomialsEvalRep(Fp, omega3, 8 * n)
    roots3 = [omega3 ** i for i in range(8 * n)]
    S1, S2, S3 = Ss
    S1_ext3 = PolyEvalRep3.from_coeffs(S1.to_coeffs())
    S2_ext3 = PolyEvalRep3.from_coeffs(S2.to_coeffs())
    S3_ext3 = PolyEvalRep3.from_coeffs(S3.to_coeffs())
    p_i_poly_ext3 = PolyEvalRep3.from_coeffs(p_i_poly.to_coeffs())
    qs_ext3 = [PolyEvalRep3.from_coeffs(q.to_coeffs()) for q in Qs]
    q_L_ext3, q_R_ext3, q_M_ext3, q_O_ext3, q_C_ext3 = qs_ext3

    # Following the paper, we are using the Fiat Shamir Heuristic. We are
    # Simulating 5 rounds of communication with the verifier using a
    # random oracle for verifier answers
    print("Starting Round 1...")

    # Generate "random" blinding scalars
    rand_scalars = [random_fp_seeded("1234") for i in range(9)]

    # Generate polys with the random scalars as coefficients and convert to
    # evaluation representation. These are needed for zero knowledge to
    # obfuscate the witness.
    a_blind_poly_ext = Poly([rand_scalars[1], rand_scalars[0]])
    b_blind_poly_ext = Poly([rand_scalars[3], rand_scalars[2]])
    c_blind_poly_ext = Poly([rand_scalars[5], rand_scalars[4]])
    a_blind_poly_ext = PolyEvalRep2.from_coeffs(a_blind_poly_ext)
    b_blind_poly_ext = PolyEvalRep2.from_coeffs(b_blind_poly_ext)
    c_blind_poly_ext = PolyEvalRep2.from_coeffs(c_blind_poly_ext)

    # These polynomals have random evaluations at all points except ROOTS where
    # they evaluate to the witness
    a_poly_ext = a_blind_poly_ext * vanishing_poly_ext + witness_poly_a_ext
    b_poly_ext = b_blind_poly_ext * vanishing_poly_ext + witness_poly_b_ext
    c_poly_ext = c_blind_poly_ext * vanishing_poly_ext + witness_poly_c_ext

    # Evaluate the witness polynomials in the exponent using the CRS
    a_eval_exp = evaluate_in_exponent(CRS, a_poly_ext.to_coeffs())
    b_eval_exp = evaluate_in_exponent(CRS, b_poly_ext.to_coeffs())
    c_eval_exp = evaluate_in_exponent(CRS, c_poly_ext.to_coeffs())

    first_output = [a_eval_exp, b_eval_exp, c_eval_exp]
    print("Round 1 Finished with output: ", first_output)

    print("Starting Round 2...")
    # Compute permutation challenges from imaginary verifier
    beta = random_fp_seeded(str(first_output) + "0")
    gamma = random_fp_seeded(str(first_output) + "1")

    # Compute permutation polynomial. z_1 is the blinding summand needed for ZK
    z_1 = Poly([rand_scalars[8], rand_scalars[7], rand_scalars[6]])
    z_1 = PolyEvalRep2.from_coeffs(z_1)
    z_1 = z_1 * vanishing_poly_ext
    accumulator_poly_eval = [Fp(1)]
    accumulator_poly_eval += [accumulator_factor(n,
                                                 i,
                                                 witness, beta,
                                                 id_domain,
                                                 perm_domain,
                                                 gamma)
                              for i in range(n-1)]
    accumulator_poly = PolyEvalRep(ROOTS, accumulator_poly_eval)
    accumulator_poly = z_1 + PolyEvalRep2.from_coeffs(accumulator_poly.to_coeffs())

    second_output = evaluate_in_exponent(CRS, accumulator_poly.to_coeffs())
    print("Round 2 Finished with output: ", second_output)

    print("Starting Round 3...")
    alpha = random_fp_seeded(str(first_output) + str(second_output))

    accumulator_poly_ext3 = PolyEvalRep3.from_coeffs(accumulator_poly.to_coeffs())

    # The third summand of t has the accumulator poly evaluated at a shift
    accumulator_poly_shift_evaluations = accumulator_poly.evaluate(roots3, ROOTS[1])
    accumulator_poly_ext3_shift = PolyEvalRep3(roots3,
                                               accumulator_poly_shift_evaluations)

    a_poly_ext3 = PolyEvalRep3.from_coeffs(a_poly_ext.to_coeffs())
    b_poly_ext3 = PolyEvalRep3.from_coeffs(b_poly_ext.to_coeffs())
    c_poly_ext3 = PolyEvalRep3.from_coeffs(c_poly_ext.to_coeffs())

    id_poly_1_ext3 = PolyEvalRep3.from_coeffs(Poly([gamma, beta]))
    id_poly_2_ext3 = PolyEvalRep3.from_coeffs(Poly([gamma, beta * k]))
    id_poly_3_ext3 = PolyEvalRep3.from_coeffs(Poly([gamma, beta * k**2]))

    gamma_poly = PolyEvalRep3.from_coeffs(Poly([gamma]))
    L_1 = PolyEvalRep(ROOTS, [Fp(1)] + [Fp(0) for i in range(len(ROOTS)-1)])

    # Compute quotient polynomial: we are dividing by the vanishing poly which
    # has zeros at n roots so we need to do division by swapping to a coset
    # first summand should have degree 3n+1, second and third should have
    # degree 4n + 5
    t = ((a_poly_ext3 * b_poly_ext3 * q_M_ext3) +
         (a_poly_ext3 * q_L_ext3) +
         (b_poly_ext3 * q_R_ext3) +
         (c_poly_ext3 * q_O_ext3) +
         q_C_ext3 + p_i_poly_ext3)

    t += ((a_poly_ext3 + id_poly_1_ext3) *
          (b_poly_ext3 + id_poly_2_ext3) *
          (c_poly_ext3 + id_poly_3_ext3) * accumulator_poly_ext3 * alpha)

    t -= ((a_poly_ext3 + S1_ext3 * beta + gamma_poly) *
          (b_poly_ext3 + S2_ext3 * beta + gamma_poly) *
          (c_poly_ext3 + S3_ext3 * beta + gamma_poly) *
          accumulator_poly_ext3_shift * alpha)

    t += ((accumulator_poly_ext3 - PolyEvalRep3.from_coeffs(Poly([Fp(1)]))) *
          PolyEvalRep3.from_coeffs(L_1.to_coeffs()) * alpha ** 2)

    t = PolyEvalRep3.divideWithCoset(t.to_coeffs(), vanishing_pol_coeff)

    t_coeff = t.coefficients

    # We split up the polynomial t in three polynomials so that:
    # t = t_lo + x^n*t_mid + x^2n*t_hi
    # I found that n has actually to be (n+2) to accomodate the CRS because
    # t can be of degree 4n+5
    t_lo = Poly(t_coeff[:n+2])
    t_mid = Poly(t_coeff[n+2:2*(n+2)])
    t_hi = Poly(t_coeff[2*(n+2):])

    t_lo_eval_exp = evaluate_in_exponent(CRS, t_lo)
    t_mid_eval_exp = evaluate_in_exponent(CRS, t_mid)
    t_hi_eval_exp = evaluate_in_exponent(CRS, t_hi)

    third_output = [t_lo_eval_exp, t_mid_eval_exp, t_hi_eval_exp]
    print("Round 3 Finished with output: ", third_output)

    print("Starting Round 4...")
    # Compute the evaluation challenge
    zeta = random_fp_seeded(str(first_output) +
                            str(second_output) +
                            str(third_output))

    # Compute the opening evaluations
    a_zeta = a_poly_ext.evaluate([zeta])[0]
    b_zeta = b_poly_ext.evaluate([zeta])[0]
    c_zeta = c_poly_ext.evaluate([zeta])[0]
    S_1_zeta = S1.evaluate([zeta])[0]
    S_2_zeta = S2.evaluate([zeta])[0]
    t_zeta = PolyEvalRep3.from_coeffs(t).evaluate([zeta])[0]
    accumulator_shift_zeta = accumulator_poly_ext3.evaluate([zeta * ROOTS[1]])[0]

    # Compute linerisation polynomial
    r = (q_M_ext3 * a_zeta * b_zeta +
         q_L_ext3 * a_zeta +
         q_R_ext3 * b_zeta +
         q_O_ext3 * c_zeta +
         q_C_ext3)
    r += (accumulator_poly_ext3 *
          (a_zeta + beta * zeta + gamma) *
          (b_zeta + beta * k * zeta + gamma) *
          (c_zeta + beta * (k ** 2) * zeta + gamma) * alpha)
    r -= (S3_ext3 *
          (a_zeta + beta * S_1_zeta + gamma) *
          (b_zeta + beta * S_2_zeta + gamma) *
          alpha * beta * accumulator_shift_zeta)
    r += accumulator_poly_ext3 * L_1.evaluate([zeta])[0] * alpha ** 2

    # Evaluate r at zeta
    r_zeta = r.evaluate([zeta])[0]

    fourth_output = [a_zeta, b_zeta, c_zeta, S_1_zeta, S_2_zeta,
                     accumulator_shift_zeta, t_zeta, r_zeta]
    print("Round 4 Finished with output: ", fourth_output)

    print("Starting Round 5...")
    # Compute opening challenge
    nu = random_fp_seeded(str(first_output) +
                          str(second_output) +
                          str(third_output) +
                          str(fourth_output))

    # Compute opening proof polynomial
    W_zeta = (PolyEvalRep3.from_coeffs(t_lo) +
              PolyEvalRep3.from_coeffs(t_mid) * zeta ** (n+2) +
              PolyEvalRep3.from_coeffs(t_hi) * zeta ** (2*(n+2)) -
              PolyEvalRep3.from_coeffs(Poly([t_zeta])) +
              (r - PolyEvalRep3.from_coeffs(Poly([r_zeta]))) * nu +
              (a_poly_ext3 - PolyEvalRep3.from_coeffs(Poly([a_zeta]))) * nu ** 2 +
              (b_poly_ext3 - PolyEvalRep3.from_coeffs(Poly([b_zeta]))) * nu ** 3 +
              (c_poly_ext3 - PolyEvalRep3.from_coeffs(Poly([c_zeta]))) * nu ** 4 +
              (S1_ext3 - PolyEvalRep3.from_coeffs(Poly([S_1_zeta]))) * nu ** 5 +
              (S2_ext3 - PolyEvalRep3.from_coeffs(Poly([S_2_zeta]))) * nu ** 6)
    W_zeta = W_zeta / PolyEvalRep3.from_coeffs(Poly([-zeta, Fp(1)]))

    # Compute the opening proof polynomial
    W_zeta_omega = accumulator_poly_ext3 - PolyEvalRep3.from_coeffs(Poly([accumulator_shift_zeta]))
    W_zeta_omega = W_zeta_omega / PolyEvalRep3.from_coeffs(Poly([-zeta*ROOTS[1], Fp(1)]))

    W_zeta_eval_exp = evaluate_in_exponent(CRS, W_zeta.to_coeffs())
    W_zeta_omega_eval_exp = evaluate_in_exponent(CRS, W_zeta_omega.to_coeffs())

    fifth_output = [W_zeta_eval_exp, W_zeta_omega_eval_exp]
    proof_SNARK = [first_output, second_output, third_output, fifth_output, fourth_output]
    print("Round 5 Finished with output: ", fifth_output)

    u = random_fp_seeded(str(proof_SNARK))
    return proof_SNARK, u

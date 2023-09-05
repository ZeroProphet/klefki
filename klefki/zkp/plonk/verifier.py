from .polynomial_evalrep import get_omega
from .polynomial_evalrep import polynomialsEvalRep
from .ssbls12 import Fp, Group, random_fp_seeded


G = Group.G
G2 = Group.G


def verifier_algo(proof_SNARK, n, p_i_poly, verifier_preprocessing, k):
    print("Starting Verification...")
    omega = get_omega(Fp, n)

    first_output, second_output, third_output, fifth_output, fourth_output = proof_SNARK
    a_eval_exp, b_eval_exp, c_eval_exp = first_output
    z_eval_exp = second_output
    t_lo_eval_exp, t_mid_eval_exp, t_hi_eval_exp = third_output
    a_zeta, b_zeta, c_zeta, S_1_zeta, S_2_zeta, accumulator_shift_zeta, t_zeta, r_zeta = fourth_output
    W_zeta_eval_exp, W_zeta_omega_eval_exp = fifth_output

    q_exp, s_exp, x_exp = verifier_preprocessing
    q_L_exp, q_R_exp, q_M_exp, q_O_exp, q_C_exp = q_exp
    s_1_exp, s_2_exp, s_3_exp = s_exp

    print("Check1: Elements in group?")
    assert type(a_eval_exp) is Group
    assert type(b_eval_exp) is Group
    assert type(c_eval_exp) is Group
    assert type(z_eval_exp) is Group
    assert type(t_lo_eval_exp) is Group
    assert type(t_mid_eval_exp) is Group
    assert type(t_hi_eval_exp) is Group
    assert type(W_zeta_eval_exp) is Group
    assert type(W_zeta_omega_eval_exp) is Group

    print("Check2: Elements in field?")
    assert type(a_zeta) is Fp
    assert type(b_zeta) is Fp
    assert type(c_zeta) is Fp
    assert type(S_1_zeta) is Fp
    assert type(S_2_zeta) is Fp
    assert type(r_zeta) is Fp
    assert type(accumulator_shift_zeta) is Fp

    print("Check3: Public input in field?")
    print(type(p_i_poly))
    assert type(p_i_poly) == polynomialsEvalRep(Fp, omega, n)

    print("Step4: Recompute challenges from transcript")
    beta = random_fp_seeded(str(first_output) + "0")
    gamma = random_fp_seeded(str(first_output) + "1")
    alpha = random_fp_seeded(str(first_output) + str(second_output))
    zeta = random_fp_seeded(str(first_output) +
                            str(second_output) +
                            str(third_output))
    nu = random_fp_seeded(str(first_output) +
                          str(second_output) +
                          str(third_output) +
                          str(fourth_output))
    u = random_fp_seeded(str(proof_SNARK))

    print("Step5: Evaluate vanishing polynomial at zeta")
    vanishing_poly_eval = zeta ** n - Fp(1)

    print("Step6: Evaluate lagrange polynomial at zeta")
    L_1_zeta = (zeta ** n - Fp(1)) / ((zeta - Fp(1)) * n)

    print("Step7: Evaluate public input polynomial at zeta")
    p_i_poly_zeta = p_i_poly.evaluate([zeta])[0]

    print("Step8: Compute quotient polynomial evaluation")
    t_zeta = (r_zeta + p_i_poly_zeta -
              (a_zeta + beta * S_1_zeta + gamma) *
              (b_zeta + beta * S_2_zeta + gamma) *
              (c_zeta + gamma) * accumulator_shift_zeta * alpha -
              L_1_zeta * alpha ** 2) / vanishing_poly_eval

    print("Step9: Compute first part of batched polynomial commitment")
    D_1_exp = (q_M_exp * a_zeta * b_zeta * nu +
               q_L_exp * a_zeta * nu +
               q_R_exp * b_zeta * nu +
               q_O_exp * c_zeta * nu +
               q_C_exp * nu)
    D_1_exp += (z_eval_exp * (
                (a_zeta + beta * zeta + gamma) *
                (b_zeta + beta * k * zeta + gamma) *
                (c_zeta + beta * (k ** 2) * zeta + gamma) * alpha * nu
                + L_1_zeta * (alpha ** 2) * nu + u))
    D_1_exp += (s_3_exp *
                (a_zeta + beta * S_1_zeta + gamma) *
                (b_zeta + beta * S_2_zeta + gamma) *
                alpha * beta * accumulator_shift_zeta * nu) * Fp(-1)

    print("Step10: Compute full batched polynomial commitment")
    F_1_exp = (t_lo_eval_exp +
               t_mid_eval_exp * zeta ** (n+2) +
               t_hi_eval_exp * zeta ** (2*(n+2)) +
               D_1_exp +
               a_eval_exp * nu ** 2 +
               b_eval_exp * nu ** 3 +
               c_eval_exp * nu ** 4 +
               s_1_exp * nu ** 5 +
               s_2_exp * nu ** 6)

    print("Step 11: Compute group encoded batch evaluation")
    E_1_exp = G * (t_zeta +
                   nu * r_zeta +
                   nu ** 2 * a_zeta +
                   nu ** 3 * b_zeta +
                   nu ** 4 * c_zeta +
                   nu ** 5 * S_1_zeta +
                   nu ** 6 * S_2_zeta +
                   u * accumulator_shift_zeta)

    print("Check12: Batch validate all evaluations via pairing")
    e11 = W_zeta_eval_exp + W_zeta_omega_eval_exp * u
    e21 = (W_zeta_eval_exp * zeta + W_zeta_omega_eval_exp * u * zeta * omega +
           F_1_exp + (E_1_exp * Fp(-1)))
    assert e11.pair(x_exp) == e21.pair(G2)
    print("Verification Successful!")

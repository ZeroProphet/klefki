from zkp_playground.algebra.utils import randfield

from .polynomial_evalrep import get_omega
from .polynomial_evalrep import polynomialsEvalRep
from .ssbls12 import Fp, Group, evaluate_in_exponent

G = Group.G
G2 = Group.G


def setup_algo(gates_matrix, permutation, L, p_i):
    print("Starting Setup Phase...")
    (m, n) = len(gates_matrix), len(gates_matrix[0])

    omega = get_omega(Fp, n)
    ROOTS = [omega ** i for i in range(n)]

    PolyEvalRep = polynomialsEvalRep(Fp, omega, n)

    # Generate polynomials from columns of gates_matrix
    q_L = PolyEvalRep(ROOTS, [Fp(i) for i in gates_matrix[0]])
    q_R = PolyEvalRep(ROOTS, [Fp(i) for i in gates_matrix[1]])
    q_M = PolyEvalRep(ROOTS, [Fp(i) for i in gates_matrix[2]])
    q_O = PolyEvalRep(ROOTS, [Fp(i) for i in gates_matrix[3]])
    q_C = PolyEvalRep(ROOTS, [Fp(i) for i in gates_matrix[4]])
    Qs = [q_L, q_R, q_M, q_O, q_C]

    # The public input poly vanishes everywhere except for the position of the
    # public input gate where it evaluates to -(public_input)
    public_input = [Fp(0) for i in range(len(ROOTS))]
    for i in L:
        public_input[i] = Fp(-p_i)
    p_i_poly = PolyEvalRep(ROOTS, public_input)

    # We generate domains on which we can evaluate the witness polynomials
    k = randfield(Fp)
    id_domain_a = ROOTS
    id_domain_b = [k * root for root in ROOTS]
    id_domain_c = [k**2 * root for root in ROOTS]
    id_domain = id_domain_a + id_domain_b + id_domain_c

    # We permute the positions of the domain generated above
    perm_domain = [id_domain[i - 1] for i in permutation]
    perm_domain_a = perm_domain[:n]
    perm_domain_b = perm_domain[n: 2*n]
    perm_domain_c = perm_domain[2*n:3*n]

    # Generate polynomials that return the permuted index when evaluated on the
    # domain
    S_sigma_1 = PolyEvalRep(ROOTS, perm_domain_a)
    S_sigma_2 = PolyEvalRep(ROOTS, perm_domain_b)
    S_sigma_3 = PolyEvalRep(ROOTS, perm_domain_c)
    Ss = [S_sigma_1, S_sigma_2, S_sigma_3]

    perm_precomp = [id_domain, perm_domain, k, Ss]

    # We perform the trusted setup
    tau = randfield(Fp)
    CRS = [G * (tau ** i) for i in range(n + 3)]

    # We take some work off the shoulders of the verifier
    print("Starting Verifier Preprocessing...")
    q_exp = [evaluate_in_exponent(CRS, q.to_coeffs()) for q in Qs]
    s_exp = [evaluate_in_exponent(CRS, s.to_coeffs()) for s in Ss]
    x_exp = G2 * tau
    verifier_preprocessing = [q_exp, s_exp, x_exp]
    print("Setup Phase Finished!")

    return CRS, Qs, p_i_poly, perm_precomp, verifier_preprocessing


import sys
import numpy as np
from setup import setup_algo
from prover import prover_algo
from verifier import verifier_algo


def permute_idices(wires):
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


def test_plonk():
    # Wires
    a = ["x", "var1", "var2", "1", "1", "var3", "empty1", "empty2"]
    b = ["x", "x", "x", "5", "35", "5", "empty3", "empty4"]
    c = ["var1", "var2", "var3", "5", "35", "35", "empty5", "empty6"]

    wires = a + b + c

    # Gates
    add = np.array([1, 1, 0, -1, 0])
    mul = np.array([0, 0, 1, -1, 0])
    const5 = np.array([0, 1, 0, 0, -5])
    public_input = np.array([0, 1, 0, 0, 0])
    empty = np.array([0, 0, 0, 0, 0])

    gates_matrix = np.array([mul, mul, add, const5, public_input, add, empty, empty])
    permutation = permute_idices(wires)
    # We can provide public input 35. For that we need to specify the position
    # of the gate in L and the value of the public input in p_i
    L = [4]
    p_i = 35

    n = len(gates_matrix)
    gates_matrix = gates_matrix.transpose()

    # To get the witness, the prover applies his private input x=3 to the
    # circuit and writes down the value of every wire.
    witness = [
        3,
        9,
        27,
        1,
        1,
        30,
        0,
        0,
        3,
        3,
        3,
        5,
        35,
        5,
        0,
        0,
        9,
        27,
        30,
        5,
        35,
        35,
        0,
        0,
    ]

    # We start with a setup that computes the trusted setup and does some
    # precomputation
    CRS, Qs, p_i_poly, perm_prep, verifier_prep = setup_algo(
        gates_matrix, permutation, L, p_i
    )
    # The prover calculates the proof
    proof_SNARK, u = prover_algo(witness, CRS, Qs, p_i_poly, perm_prep)

    # Verifier checks if proof checks out
    verifier_algo(proof_SNARK, n, p_i_poly, verifier_prep, perm_prep[2])


test_plonk()

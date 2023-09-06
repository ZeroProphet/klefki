"""
from https://github.com/ethereum/research/blob/master/zksnark/code_to_r1cs.py
ref: https://medium.com/@VitalikButerin/quadratic-arithmetic-programs-from-zero-to-hero-f6d558cea649
"""

import inspect
from zkp_playground.zkp.zkpy import Flattener
import types


# Adds a variable or number into one of the vectors; if it's a variable
# then the slot associated with that variable is set to 1, and if it's
# a number then the slot associated with 1 gets set to that number
def insert_var(arr, varz, var, used, reverse=False):
    if isinstance(var, str):
        if var not in used:
            raise Exception("Using a variable before it is set!")
        arr[varz.index(var)] += (-1 if reverse else 1)
    elif isinstance(var, int):
        arr[0] += var * (-1 if reverse else 1)

# Maps input, output and intermediate variables to indices


def get_var_placement(inputs, flatcode):
    return ['~one'] + [x for x in inputs] + ['~out'] + [
        c[1] for c in flatcode if c[1] not in inputs and c[1] != '~out']


# Convert the flattened code generated above into a rank-1 constraint system
def flatcode_to_r1cs(inputs, flatcode, field=int):
    # f.var
    # [~one, inputs, ~out, temp_vars]
    varz = get_var_placement(inputs, flatcode)
    A, B, C = [], [], []

    # [true, true, true, ...]
    used = {i: True for i in inputs}

    for x in flatcode:
        (a, b, c) = (
            [field(0)] * len(varz),
            [field(0)] * len(varz),
            [field(0)] * len(varz)
        )
        # op var expr
        (op, sym, expr) = (
            x[0],
            x[1],
            x[2:]
        )
        if sym in used:
            raise Exception("Variable already used: %r" % x[1])

        used[sym] = True

        if op == 'set':
            a[varz.index(sym)] += field(1)
            insert_var(a, varz, x[2], used, reverse=True)
            b[0] = field(1)
        elif op == 'add' or op == 'sub':
            c[varz.index(sym)] = field(1)
            insert_var(a, varz, expr[0], used)
            insert_var(a, varz, expr[1], used, reverse=(op == 'sub'))
            b[0] = field(1)
        elif op == 'mul':
            c[varz.index(sym)] = field(1)
            insert_var(a, varz, expr[0], used)
            insert_var(b, varz, expr[1], used)
        elif op == 'div':
            a[varz.index(sym)] = field(1)
            insert_var(c, varz, expr[0], used)
            insert_var(b, varz, expr[1], used)

        A.append(a)
        B.append(b)
        C.append(c)

    return A, B, C

# Get a variable or number given an existing input vector


def grab_var(varz, assignment, var):
    if isinstance(var, str):
        return assignment[varz.index(var)]
    elif isinstance(var, int):
        return var
    else:
        raise Exception("What kind of expression is this? %r" % var)

# Goes through flattened code and completes the input vector


def assign_variables(inputs, input_vars, flatcode, field):
    varz = get_var_placement(inputs, flatcode)

    assignment = [field(0)] * len(varz)
    assignment[0] = field(1)
    for i, inp in enumerate(input_vars):
        assignment[i + 1] = field(inp)
    for x in flatcode:
        assignment[varz.index(x[1])] = {
            "set": lambda: field(grab_var(varz, assignment, x[2])),
            "add": lambda: field(grab_var(varz, assignment, x[2])) + field(grab_var(varz, assignment, x[3])),
            "sub": lambda: field(grab_var(varz, assignment, x[2])) - field(grab_var(varz, assignment, x[3])),
            "mul": lambda: field(grab_var(varz, assignment, x[2])) * field(grab_var(varz, assignment, x[3])),
            "div": lambda: field(grab_var(varz, assignment, x[2])) / field(grab_var(varz, assignment, x[3]))
        }[x[0]]()
    return assignment


def code_to_r1cs_with_inputs(code, input_vars, field):
    flatten = Flattener(code)
    inputs = flatten.inputs
    flatcode = flatten.flatten_code
    A, B, C = flatcode_to_r1cs(inputs, flatcode, field)
    r = assign_variables(inputs, input_vars, flatcode, field)
    return r, A, B, C


def mul(a, b):
    return list(map(lambda x: x[0] * x[1], zip(a, b)))


class R1CS:

    @staticmethod
    def parse(code, input_vals, field=int):
        s, A, B, C = code_to_r1cs_with_inputs(code, input_vals, field)
        return (s, A, B, C)

    @staticmethod
    def verify(s, A, B, C):
        ret = True
        for i in range(len(A)):
            ret = ret and sum(mul(A[i], s)) * \
                sum(mul(B[i], s)) == sum(mul(C[i], s))
        return ret

    @staticmethod
    def r1cs(fn_or_field=int, ctx={}):
        def wrapper(f):
            src = inspect.getsource(f)
            flatten = Flattener(src, ctx)
            f.inputs = flatten.inputs
            f.flatcode = flatten.flatten_code
            f.r1cs = flatcode_to_r1cs(f.inputs, f.flatcode, field)
            f.A = f.r1cs[0]
            f.B = f.r1cs[1]
            f.C = f.r1cs[2]
            f.var = get_var_placement(f.inputs, f.flatcode)
            f.src = src

            def wit(*args):
                return assign_variables(f.inputs, args, f.flatcode, field)
            f.witness = wit
            return f
        if isinstance(fn_or_field, types.FunctionType):
            f = fn_or_field
            field = int
            return wrapper(f)
        else:
            field = fn_or_field
            return wrapper

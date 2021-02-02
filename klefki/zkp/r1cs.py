"""
from https://github.com/ethereum/research/blob/master/zksnark/code_to_r1cs.py
ref: https://medium.com/@VitalikButerin/quadratic-arithmetic-programs-from-zero-to-hero-f6d558cea649
"""

from time import time
import ast
import inspect

class Flattener:
    def __init__(self, src):
        raw = ast.parse(src).body
        assert len(raw) == 1 and isinstance(raw[0], ast.FunctionDef), "only support function"
        self.raw = raw[0]
        self.extra_inputs()
        self.extra_body()
        self._symbol = 0
        self.flatten_body()

    def mk_symbol(self):
        ret = "Sym-%s" % str(self._symbol)
        self._symbol += 1
        return ret

    def extra_inputs(self):
        self.inputs = [arg.arg for arg in self.raw.args.args]

    def extra_body(self):
        body = []
        avalid_stmt = (ast.Assign, ast.Return)
        returned = False
        for c in self.raw.body:
            assert isinstance(c, avalid_stmt)
            assert not returned
            if isinstance(c, ast.Return):
                returned = True
            body.append(c)
        self.body = body

    def flatten_body(self):
        self.flatten_code = sum([self.flatten_stmt(c) for c in self.body], [])


    def flatten_stmt(self, s):
        if isinstance(s, ast.Assign):
            assert len(s.targets) == 1 and isinstance(s.targets[0], ast.Name)
            target = s.targets[0].id

        elif isinstance(s, ast.Return):
            target = '~out'
        # Get inner content
        return self.flatten_expr(target, s.value)

    def flatten_expr(self, target, expr):
        # x = y
        if isinstance(expr, ast.Name):
            return [['set', target, expr.id]]
        # x = 5
        elif isinstance(expr, ast.Num):
            return [['set', target, expr.n]]

        elif isinstance(expr, ast.BinOp):
            return self.flatten_binop(target, expr)

    def flatten_binop(self, target, expr):
        avalid_binop = (ast.Mult, ast.Add, ast.Sub, ast.Div, ast.Pow)
        assert type(expr.op) in avalid_binop
        if isinstance(expr.op, ast.Add):
            op = '+'
        elif isinstance(expr.op, ast.Mult):
            op = '*'
        elif isinstance(expr.op, ast.Sub):
            op = '-'
        elif isinstance(expr.op, ast.Div):
            op = '/'
        elif isinstance(expr.op, ast.Pow):
            return self.flatten_pow(target, expr)

        if isinstance(expr.left, (ast.Name, ast.Num)):
            var1 = expr.left.id if isinstance(expr.left, ast.Name) else expr.left.n
            sub1 = []
        # If one of the subexpressions is itself a compound expression, recursively
        # apply this method to it using an intermediate variable
        else:
            var1 = self.mk_symbol()
            sub1 = self.flatten_expr(var1, expr.left)
        # Same for right subexpression as for left subexpression
        if isinstance(expr.right, (ast.Name, ast.Num)):
            var2 = expr.right.id if isinstance(expr.right, ast.Name) else expr.right.n
            sub2 = []
        else:
            var2 = self.mk_symbol()
            sub2 = self.flatten_expr(var2, expr.right)
        # Last expression represents the assignment; sub1 and sub2 represent the
        # processing for the subexpression if any
        return sub1 + sub2 + [[op, target, var1, var2]]


    def flatten_pow(self, target, expr):
        assert isinstance(expr.right, ast.Num)
        if expr.right.n == 0:
            return [['set', target, 1]]
        elif expr.right.n == 1:
            return self.flatten_expr(target, expr.left)
        else: # This could be made more efficient via square-and-multiply but oh well
            if isinstance(expr.left, (ast.Name, ast.Num)):
                nxt = base = expr.left.id if isinstance(expr.left, ast.Name) else expr.left.n
                o = []
            else:
                nxt = base = self.mk_symbol()
                o = self.flatten_expr(base, expr.left)
            for i in range(1, expr.right.n):
                latest = nxt
                nxt = target if i == expr.right.n - 1 else self.mk_symbol()
                o.append(['*', nxt, latest, base])
            return o



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
    varz = get_var_placement(inputs, flatcode)
    A, B, C = [], [], []
    used = {i: True for i in inputs}
    for x in flatcode:
        a, b, c = [field(0)] * len(varz), [field(0)] * len(varz), [field(0)] * len(varz)
        if x[1] in used:
            raise Exception("Variable already used: %r" % x[1])
        used[x[1]] = True
        if x[0] == 'set':
            a[varz.index(x[1])] += field(1)
            insert_var(a, varz, x[2], used, reverse=True)
            b[0] = 1
        elif x[0] == '+' or x[0] == '-':
            c[varz.index(x[1])] = field(1)
            insert_var(a, varz, x[2], used)
            insert_var(a, varz, x[3], used, reverse=(x[0] == '-'))
            b[0] = 1
        elif x[0] == '*':
            c[varz.index(x[1])] = field(1)
            insert_var(a, varz, x[2], used)
            insert_var(b, varz, x[3], used)
        elif x[0] == '/':
            insert_var(c, varz, x[2], used)
            a[varz.index(x[1])] = field(1)
            insert_var(b, varz, x[3], used)
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
            "set": field(grab_var(varz, assignment, x[2])),
            "+": field(grab_var(varz, assignment, x[2])) + field(grab_var(varz, assignment, x[3])),
            "-": field(grab_var(varz, assignment, x[2])) - field(grab_var(varz, assignment, x[3])),
            "*": field(grab_var(varz, assignment, x[2])) * field(grab_var(varz, assignment, x[3])),
            "/": field(grab_var(varz, assignment, x[2])) / field(grab_var(varz, assignment, x[3]))
        }[x[0]]
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
        for i in range(len(s)-2):
            ret = ret and sum(mul(A[i], s)) * sum(mul(B[i], s)) == sum(mul(C[i], s))
        return ret

    @staticmethod
    def r1cs(f, field=int):
        src = inspect.getsource(f)
        flatten = Flattener(src)
        inputs = flatten.inputs
        f.flatcode = flatten.flatten_code
        f.r1cs = flatcode_to_r1cs(inputs, f.flatcode, field)
        f.A = f.r1cs[0]
        f.B = f.r1cs[1]
        f.C = f.r1cs[2]
        f.var = get_var_placement(inputs, f.flatcode)
        f.src = src
        def wit(*args):
            return assign_variables(inputs, args, f.flatcode, field)
        f.witness = wit
        return f

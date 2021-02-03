import ast
from time import time

class Flattener:
    def __init__(self, src):
        raw = ast.parse(src).body
        assert len(raw) == 1 and isinstance(raw[0], ast.FunctionDef), "only support function"
        self.raw = raw[0]
        self.extra_inputs()
        self.syms = [i for i in self.inputs]
        self.extra_body()
        self._symbol = 0
        self.flatten_body()

    def mk_symbol(self, base="Sym"):
        ret = "%s-%s" % (base, str(self._symbol))
        self._symbol += 1
        return ret

    def latest_sym(self, base="Sym"):
        return [s for s in self.syms if base in s][-1]

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
            if target in self.syms:
                target = self.mk_symbol(target)
            self.syms.append(target)

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
            if isinstance(expr.left, ast.Name):
                var1 = self.latest_sym(expr.left.id)
            else:
                var1 = expr.left.n
            sub1 = []
        # If one of the subexpressions is itself a compound expression, recursively
        # apply this method to it using an intermediate variable
        else:
            var1 = self.mk_symbol()
            sub1 = self.flatten_expr(var1, expr.left)
        # Same for right subexpression as for left subexpression
        if isinstance(expr.right, (ast.Name, ast.Num)):
            if isinstance(expr.right, ast.Name):
                var2 = self.latest_sym(expr.right.id)
            else:
                var2 = expr.right.n
            sub2 = []
        else:
            var2 = self.mk_symbol()
            sub2 = flatten_expr(var2, expr.right)
        # Last expression represents the assignment; sub1 and sub2 represent the
        # processing for the subexpression if any
        return sub1 + sub2 + [[op, target, var1, var2]]


    def flatten_pow(self, target, expr):
        assert isinstance(expr.right, ast.Num)
        if expr.right.n == 0:
            return [['set', target, 1]]
        elif expr.right.n == 1:
            return flatten_expr(target, expr.left)
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

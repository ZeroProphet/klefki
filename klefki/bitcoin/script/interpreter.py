from functools import wraps
from .consts import CONSTS


class Stack(object):

    ops = {}

    def __init__(self, script):
        self.storage = []
        self.script = script
        self._output = []

    @classmethod
    def register(self, op):
        def _(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                self.ops[op] = fn
                return fn(*args, **kwargs)
            return wrapper
        return _

    def eval(self):
        return self.ops.get(self.script[0])(self, self.script)

    @property
    def output(self):
        return self._output

    @output.setter
    def set_output(self, v):
        self._output.append(v)

    def isEmpty(self):
        return len(self.storage) == 0

    def push(self, p):
        self.storage[:0] = p
        return self

    def pop(self, p):
        return self.pop(p)

    def __repr__(self):
        return self.storage.__repr__()


@Stack.register(CONSTS.OP_0)
def op_0(stack, script):
    stack.push([])
    stack.ouput = ''
    return stack.eval(script[1], stack, script[1:])


def op_pushdata(stack, script, n):
    next_n_bytes = script[0:n]
    count = int(next_n_bytes.hex(), 16)
    stack.push(script[n: count + n])
    stack.output = next_n_bytes
    return stack.eval(script[count + n], stack, script[count + n:])


@Stack.register(CONSTS.OP_PUSHDATA1)
def op_pushdata1(stack, script):
    return op_pushdata(stack, script, 1)


@Stack.register(CONSTS.OP_PUSHDATA2)
def op_pushdata2(stack, script):
    return op_pushdata(stack, script, 2)


@Stack.register(CONSTS.OP_PUSHDATA3)
def op_pushdata3(stack, script):
    return op_pushdata(stack, script, 3)


def op_pushdata4(stack, script):
    return op_pushdata(stack, script, 4)


def op_1negate(stack, script):
    stack.push(-1)
    stack.output = -1
    return stack.eval(script[1], stack, script[1:])


def op_1(stack, script):
    stack.push(1)
    stack.output = 1
    return stack.eval(script[1], stack, script[1:])

from .consts import FLOW_CONTROL, CONSTS


def op_exec(op, stack, index):
    return {
        FLOW_CONTROL.OP_IF: op_if,
        FLOW_CONTROL.OP_NOIF: op_noif,
        FLOW_CONTROL.OP_ELSE: op_else,
        FLOW_CONTROL.OP_ENDIF: op_endif
    }.get(op)(stack, index)


def op_else(stack, index):
    return op_exec(stack[index + 1], stack)


def op_if(stack, index):
    if stack.pop(index) != CONSTS.OP_FALSE:
        return op_exec(stack[index], stack, 0)
    else:
        return op_exec(stack[index + 1], stack, 1)


def op_noif(stack, index):
    if stack.pop(index) == CONSTS.OP_FALSE:
        return op_exec(stack[index], stack, 0)
    else:
        return op_exec(stack[index + 1], stack, 1)


def op_endif(stack, index):
    stack = stack[index:]
    return op_exec(stack[0], stack, 0)

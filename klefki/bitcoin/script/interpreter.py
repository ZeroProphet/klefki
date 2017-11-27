from .consts import FLOW_CONTROL, CONSTS


def op_exec(op, stack, index):
    return {
        FLOW_CONTROL.OP_IF: op_if,
        FLOW_CONTROL.OP_NOIF: op_noif,
        FLOW_CONTROL.OP_ELSE: op_else
    }.get(op)(stack, index)


def op_else(stack, index):
    return op_exec(stack[index], stack)


def op_if(stack, index):
    if stack.pop(0) != CONSTS.OP_FALSE:
        return op_exec(stack[0], stack, 0)
    elif stack[1] == FLOW_CONTROL.OP_ELSE:
        return op_exec(stack[2], stack, 2)
    elif stack[1] == FLOW_CONTROL.OP_ENDIF:
        return op_exec(stack[2], stack[1:], 2)


def op_noif(stack, index):
    if stack.pop(0) == CONSTS.OP_FALSE:
        return op_exec(stack[0], stack, 0)
    elif stack[1] == FLOW_CONTROL.OP_ELSE:
        return op_exec(stack[2], stack, 2)
    elif stack[1] == FLOW_CONTROL.OP_ENDIF:
        return op_exec(stack[2], stack[1:], 2)

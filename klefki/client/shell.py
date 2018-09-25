from functools import wraps, partial
import sys

def command(fn, name=None):

    if not hasattr(command, 'registered'):
        command.registered = {}
    fname = name or fn.__name__
    command.registered[fname] = fn
    return fn

@command
def shell():
    '''
    default Shell
    '''
    import random
    from klefki.utils import to_sha256int
    from klefki.types.algebra.concrete import (
        JacobianGroupSecp256k1 as JG,
        EllipticCurveCyclicSubgroupSecp256k1 as CG,
        EllipticCurveGroupSecp256k1 as ECG,
        FiniteFieldCyclicSecp256k1 as CF
    )
    import IPython
    N = CG.N
    G = CG.G
    IPython.embed()


@command
def help():
    '''
    This help command
    '''
    for k, v in command.registered.items():
        print(k, v.__doc__)


def not_found(cmd):
    print('cmd %s not found' % cmd)
    return


def output(fn):
    @wraps(fn)
    def _(*args, **kwargs):
        return print(fn(*args, **kwargs))
    return _


def router(cmds):
    'fn a b c=1 d=2'
    if isinstance(cmds, str):
        cmds = cmds.split(' ')
    try:
        fn = command.registered.get(cmds[0], None)
    except IndexError as _:
        return help()
    if not fn:
        return not_found(cmds)
    args = [c for c in cmds[1:] if '=' not in c]
    kwargs = dict([c.split('=') for c in cmds[1:] if '=' in c])
    return fn(*args, **kwargs)


main = partial(router, cmds=sys.argv[1:])


if __name__ == "__main__":
    main()

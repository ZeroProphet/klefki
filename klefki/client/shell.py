def command(fn, name=None):

    if not hasattr(command, 'registered'):
        command.registered = {}
    fname = name or fn.__name__
    command.registered[fname] = fn

    return fn


def not_found():
    print('cmd not found')
    return


def router(cmd: str):
    'fn a b c=1 d=2'
    cmds = cmd.split(' ')
    fn = command.registered.get(cmds[0], None)
    if not fn:
        return not_found()
    args = [c for c in cmds if '=' not in cmds[1:]]
    kwargs = dict([c.split('=') for c in cmds if '=' in cmds[1:]])
    return fn(*args, **kwargs)

def command(fn, name=None):

    if not hasattr(command, 'registered'):
        command.registered = {}
    fname = name or fn.__name__
    command.registered[fname] = fn

    return fn


@command
def help():
    for k, v in command.registered.items():
        print(k, v)


def not_found(cmd):
    print('cmd %s not found' % cmd)
    return


def router(cmds):
    'fn a b c=1 d=2'
    if isinstance(cmds, str):
        cmds = cmds.split(' ')
    fn = command.registered.get(cmds[0], None)
    if not fn:
        return not_found(cmds)
    args = [c for c in cmds[1:] if '=' not in cmds[1:]]
    kwargs = dict([c.split('=') for c in cmds[1:] if '=' in cmds[1:]])
    return fn(*args, **kwargs)

from functools import partial
from klefki.client.shell import command


@command
def cmd():
    return


@partial(command, name='test2')
def cmd2():
    return


def test_register():
    assert command.registered == {
        'cmd': cmd,
        'test2': cmd2
    }

from functools import partial
from zkp_playground.client.shell import command, help


@command
def cmd():
    return


@partial(command, name='test2')
def cmd2():
    return


def test_register():
    assert 'cmd' in command.registered
    assert 'test2' in command.registered

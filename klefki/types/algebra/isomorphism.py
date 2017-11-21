from types import FunctionType
from functools import reduce


__all__ = ['Isomorphism']


class Isomorphism():
    '''
    A morphism f : X → Y in a category is an isomorphism if it admits a two-sided inverse.
    '''

    class Trunks(list):

        def __call__(self, *args, **kwargs):
            print(self)

            def _eval(args, fn):
                if type(args) in [list, tuple]:
                    return fn(*args)
                if type(args) is dict:
                    return fn(**args)
                else:
                    return fn(args)

            return reduce(_eval, self, kwargs or args)

        def __rshift__(self, next):
            self.append(next)
            return self

        def __lshift__(self, prev):
            self.insert(0, prev.inverse)
            return self

    def __init__(self, fn):
        assert isinstance(fn, FunctionType)
        assert hasattr(fn, 'inverse')
        self.fn = fn
        self.inverse = fn.inverse

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

    def __rshift__(self, next):
        return self.Trunks([self, next])

    def __lshift__(self, prev):
        return self.Trunks([self.inverse, prev.inverse])

    @staticmethod
    def inv(inverse):
        def _(fn):
            fn.inverse = inverse
            return fn
        return _

    def __repr__(self):
        return self.fn.__repr__()

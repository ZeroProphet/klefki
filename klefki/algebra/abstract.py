from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Callable, Iterable, Any
from operator import eq
from klefki.algorithms import double_and_add_algorithm
from klefki.algorithms import complex_truediv_algorithm
from klefki.algorithms import fast_pow
from klefki.numbers import modular_sqrt
import sys


class Functor(metaclass=ABCMeta):

    __slots__ = ['value']

    @classmethod
    def construct(cls, name, **kwargs):
        return type(name, (cls, ), dict(**kwargs))

    def __init__(self, *args):
        if len(args) == 1:
            args = args[0]
            if isinstance(args, self.type):
                self.value = args.value
            else:
                self.value = self.craft(args)
        else:
            self.value = self.craft(args)

    def craft(self, o):
        return o

    @property
    def type(self):
        return self.__class__

    @property
    def id(self):
        return self.value

    @classmethod
    def fmap(cls, f: Callable[[Any], Any]) -> Callable[["Functor"], "Functor"]:
        return lambda *xs: cls(f(*[x.id for x in xs]))

    @classmethod
    def lift_fmap(cls, f: Callable[["Functor"], "Functor"]) -> Callable[[Any], "Functor"]:
        return lambda *xs: f(*(cls(x) for x in xs))


class Groupoid(Functor):

    __slots__ = ()

    @abstractmethod
    def op(self, g: 'Group') -> 'Group':
        pass

    def __eq__(self, b) -> bool:
        return self.id == b.id

    def __lt__(self, b) -> bool:
        return self.id < b.id

    def __le__(self, b) -> bool:
        return self.id <= b.id

    def __gt__(self, b) -> bool:
        return self.id > b.id

    def __ge__(self, b) -> bool:
        return self.id >= b.id

    def __add__(self, g: 'Group') -> 'Group':
        '''
        Allowing call associativity operator via A + B
        Strict limit arg `g` and ret `res` should be subtype of Group,
        For obeying axiom `closure` (1)
        '''
        res = self.op(g)
        assert isinstance(res, type(self))
        return res

    def __radd__(self, g):
        return self.__add__(g)

    def __mul__(self, g: 'Group') -> 'Group':
        return self.__add__(g)

    def __repr__(self):
        return "%s::%s" % (
            type(self).__name__,
            self.id
        )

    def __str__(self):
        return str(self.id)


class SemiGroup(Groupoid):

    __slots__ = ()

    @abstractmethod
    def op(self, g: 'Group') -> 'Group':
        '''
        The Operator for obeying axiom `associativity` (2)
        '''
        pass


class Monoid(SemiGroup):
    __slots__ = ()

    @classmethod
    def zero(cls):
        return cls.identity()

    @classmethod
    def identity(cls):
        '''
        The value for obeying axiom `identity` (3)
        '''
        return cls(0)

    def __not__(self):
        return self is not self.identity()

    def scalar(self, times):
        while getattr(times, 'value', None) != None:
            times = times.id
        if times == 0:
            return self.identity()
        return double_and_add_algorithm(times, self, self.identity())

    def __matmul__(self, times):
        return self.scalar(times)

    def __pow__(self, times) -> 'Group':
        return self.scalar(times)

    def __xor__(self, times) -> 'Group':
        return self.__matmul__(times)


class Group(Monoid):
    __slots__ = ()

    @abstractmethod
    def inverse(self: 'Group') -> 'Group':
        '''
        Implement for axiom `inverse`
        '''
        pass

    def __sub__(self, g: 'Group') -> 'Group':
        '''
        Allow to reverse op via a - b
        '''
        return self.op(g.inverse())

    def __neg__(self) -> 'Group':
        return self.inverse()


class Ring(Group):
    __slots__ = ()

    @abstractmethod
    def sec_op(self, g: 'Field') -> 'Field':
        '''
        The Operator for obeying axiom `associativity` (2)
        '''
        pass

    def __mul__(self, g: 'Field') -> 'Field':
        '''
        Allowing call associativity operator via A * B
        Strict limit arg `g` and ret `res` should be subtype of Group,
        For obeying axiom `closure` (1)
        '''
        res = self.sec_op(g)
        assert isinstance(res, type(self)), 'result shuould be %s' % type(self)
        return res

    def __pow__(self, b, m=None):
        if hasattr(b, "value"):
            b = b.id
        if b == 0:
            return self.one()
        elif b < 0:
            return ~self.type(pow(self.id, b * -1, self.P))
        elif b == 1:
            return self
        elif b == (1/2):
            root = modular_sqrt(self.id, self.P)
            assert root != 0, "ins dont have root"
            return self.type(root)
        else:
            return fast_pow(b, self, self.type(1))


class Field(Ring):
    __slots__ = ()

    @abstractmethod
    def sec_inverse(self) -> 'Field':
        '''
        Implement for axiom `inverse`
        '''
        pass

    @classmethod
    def sec_identity(cls):
        return cls(1)

    @classmethod
    def one(cls):
        return cls.sec_identity()

    def __invert__(self):
        return self.sec_inverse()

    def __truediv__(self, g: 'Field') -> 'Field':
        if isinstance(g.id, complex):
            return complex_truediv_algorithm(complex(1), self.id, self.type)
        return self.sec_op(g.sec_inverse())

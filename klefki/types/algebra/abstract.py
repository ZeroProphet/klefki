from abc import ABCMeta, abstractmethod, abstractproperty
from klefki.algorithms import double_and_add_algorithm


class Functor(metaclass=ABCMeta):

    __slots__ = ['value']

    def __init__(self, v):
        if isinstance(v, self.__class__):
            self.value = v.value
        self.value = self.fmap(v)

    def fmap(self, o):
        return o


class Groupoid(Functor):

    __slots__ = ()

    @abstractmethod
    def op(self, g: 'Group') -> 'Group':
        pass

    def __eq__(self, b) -> bool:
        return self.value == b.value

    def __lt__(self, b) -> bool:
        return self.value < b.value

    def __le__(self, b) -> bool:
        return self.value <= b.value

    def __gt__(self, b) -> bool:
        return self.value > b.value

    def __ge__(self, b) -> bool:
        return self.value >= b.value

    def __add__(self, g: 'Group') -> 'Group':
        '''
        Allowing call associativity operator via A + B
        Strict limit arg `g` and ret `res` should be subtype of Group,
        For obeying axiom `closure` (1)
        '''
        assert isinstance(g, type(self))
        res = self.op(g)
        assert isinstance(res, type(self))
        return res

    def __repr__(self):
        return "%s::%s" % (
            type(self).__name__,
            self.value
        )

    def __str__(self):
        return str(self.value)


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

    @abstractproperty
    def identity(self):
        '''
        The value for obeying axiom `identity` (3)
        '''
        pass

    def __not__(self):
        return self is not self.identity

    def __matmul__(self, times):
        while getattr(times, 'value', None):
            times = times.value
        return double_and_add_algorithm(times, self, self.identity)


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


class Field(Group):
    __slots__ = ()

    @abstractmethod
    def sec_op(self, g: 'Group') -> 'Group':
        '''
        The Operator for obeying axiom `associativity` (2)
        '''
        pass

    @abstractmethod
    def sec_inverse(self) -> 'Group':
        '''
        Implement for axiom `inverse`
        '''
        pass

    @abstractmethod
    def sec_identity(self):
        pass

    def __invert__(self):
        return self.sec_inverse()

    def __mul__(self, g: 'Group') -> 'Group':
        '''
        Allowing call associativity operator via A * B
        Strict limit arg `g` and ret `res` should be subtype of Group,
        For obeying axiom `closure` (1)
        '''
        res = self.sec_op(g)
        assert isinstance(res, type(self)), 'result shuould be %s' % type(self)
        return res

    def __pow__(self, b):
        if b == 1:
            return self
        if b == 2:
            return self * self
        return self * (self ** (b - 1))

    def __truediv__(self, g: 'Group') -> 'Group':
        return self.sec_op(g.sec_inverse())

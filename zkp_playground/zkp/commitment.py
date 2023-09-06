from abc import ABCMeta, abstractmethod, abstractproperty


class Sigma(metaclass=ABCMeta):

    @abstractproperty
    def commit(self, m, r):
        return

    @abstractproperty
    def challenge(self, e):
        return

    @abstractproperty
    def proof(self):
        return


class Commitment(metaclass=ABCMeta):
    C = abstractproperty()
    D = abstractproperty()


class TrapdoorCommitment(Commitment):
    trapdoor = abstractproperty()

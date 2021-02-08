import abc


class NIZK(abc.ABCMeta):
    @abc.abstractmethod
    def callange(self, *args, **kwargs):
        raise NotImplemented()

    @abc.abstractmethod
    def verify(self, *args, **kwargs):
        raise NotImplemented()


class Sigma(NIZK):

    @abc.abstractmethod
    def proof(self, *args, **kwargs):
        raise NotImplemented()

    @abc.abstractmethod
    def callange(self, *args, **kwargs):
        raise NotImplemented()

    @abc.abstractmethod
    def verify(self, *args, **kwargs):
        raise NotImplemented()

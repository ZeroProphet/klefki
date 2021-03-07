from abc import ABCMeta, abstractmethod, abstractproperty

class Transformer(ABCMeta):

    def craft(self, *args):
        trans = {
            k.split(_)[1], v for k, v in self.__class__.__dict__.items()
            if "from_" in k
        }
        if type(*args) in trans.keys():
            return trans[types(*args)]

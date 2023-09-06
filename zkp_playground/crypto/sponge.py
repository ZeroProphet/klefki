from zkp_playground.algorithms import bits_little_endian_from_bytes, bytes_from_bits_little_endian


class Sponge:

    def __init__(self, b, r, f=lambda x: x[::-1]):
        assert b % 8 == 0
        assert b - r >= 8
        self.f = f
        self.b = b
        self.r = r
        self.R = [int(i) for i in "0"*r]
        self.C = [int(i) for i in "0"*(b-r)]

    @property
    def S(self):
        return self.R + self.C

    @S.setter
    def S(self, v):
        self.R = v[:self.r]
        self.C = v[self.r:]

    @classmethod
    def padding(cls, dataset: bytes, r: int):
        dataset = [int(i) for i in bits_little_endian_from_bytes(dataset)]
        left = len(dataset) % (r)
        if left != 0:
            dataset = list(dataset) + [0] * (r - left)
        assert len(dataset) % (r) == 0
        return dataset

    def absorbs(self, dataset: bytes):
        dataset = self.padding(dataset, self.r)
        for i in range(0, len(dataset) // self.r):
            m = dataset[i*self.r: i*self.r+self.r]
            for i in range(0, self.r):
                self.R[i] ^= m[i]
            self.S = self.f(self.S)

    def squeezed(self, length):
        ret = []
        for i in range((length // self.r)+1):
            ret = ret + self.R
            self.S = self.f(self.S)
        ret = "".join([str(i) for i in ret])
        return bytes_from_bits_little_endian(ret)[:length]

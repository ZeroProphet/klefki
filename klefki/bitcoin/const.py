from klefki.utils import EnumDict

__all__ = ['MAGIC']

MAGIC = EnumDict(
    dict(
        main=0xD9B4BEF9,
        testnet=0xDAB5BFFA,
        testnet3=0x0709110B
    )
)

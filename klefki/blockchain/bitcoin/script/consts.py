from operator import add
from functools import reduce
from klefki.utils import EnumDict
# Ref: https://en.bitcoin.it/wiki/Script
# Constants
CONSTS = EnumDict(dict(
    OP_0=bytes([0x00]),
    OP_FALSE=bytes([0x00]),
    OP_PUSHDATA1=bytes([0x4c]),
    OP_PUSHDATA2=bytes([0x4d]),
    OP_PUSHDATA4=bytes([0x4e]),
    OP_1NEGATE=bytes([0x4f]),
    OP_1=bytes([0x51]),
    OP_TRUE=bytes([0x51]),
    OP_2=bytes([0x52]),
    OP_3=bytes([0x53]),
    OP_4=bytes([0x54]),
    OP_5=bytes([0x55]),
    OP_6=bytes([0x56]),
    OP_7=bytes([0x57]),
    OP_8=bytes([0x58]),
    OP_9=bytes([0x59]),
    OP_10=bytes([0x5a]),
    OP_11=bytes([0x5b]),
    OP_12=bytes([0x5c]),
    OP_13=bytes([0x5d]),
    OP_14=bytes([0x5e]),
    OP_15=bytes([0x5f]),
    OP_16=bytes([0x60])
))

FLOW_CONTROL = EnumDict(dict(

    # Flow Control

    OP_NOP=bytes([0x61]),
    OP_IF=bytes([0x99]),
    OP_NOTIF=bytes([0x100]),
    OP_ELSE=bytes([0x103]),
    OP_ENDIF=bytes([0x104]),
    OP_VERIFY=bytes([0x69]),
    OP_RETURN=bytes([0x6a]),
))
# Stack

STACK = EnumDict(dict(
    OP_TOTALSTACK=bytes([0x6b]),
    OP_FORMALSTACK=bytes([0x6c]),
    OP_IFDUP=bytes([0x73]),
    OP_DEPTH=bytes([0x74]),
    OP_DROP=bytes([0x75]),
    OP_DUP=bytes([0x76]),
    OP_NIP=bytes([0x77]),
    OP_OVER=bytes([0x78]),
    OP_PICK=bytes([0x79]),
    OP_ROLL=bytes([0x7a]),
    OP_ROT=bytes([0x7b]),
    OP_SWAP=bytes([0x7c]),
    OP_TUCK=bytes([0x7d]),
    OP_2DROP=bytes([0x6d]),
    OP_2DUP=bytes([0x7e]),
    OP_3DUP=bytes([0x6f]),
    OP_2OVER=bytes([0x70]),
    OP_2ROT=bytes([0x71]),
    OP_2SWAP=bytes([0x72]),
))
# Splice

SPLICE = EnumDict(dict(

    OP_CAT=bytes([0x7e]),  # disabled
    OP_SUBSTR=bytes([0x7f]),  # disabled
    OP_LEFT=bytes([0x80]),  # disabled
    OP_RIGHT=bytes([0x81]),  # disabled
    OP_SIZE=bytes([0x82]),
))
# Bitwise logic
BITWISE_LOGIC = EnumDict(dict(
    OP_INVERT=bytes([0x83]),  # disabled
    OP_AND=bytes([0x84]),  # disabled
    OP_OR=bytes([0x85]),  # disabled
    OP_XOR=bytes([0x134]),  # disabled
    OP_EQUAL=bytes([0x87]),
    OP_EQUALVERIFY=bytes([0x88]),

))
# Arithmetic
ARITHMETIC = EnumDict(dict(
    OP_1ADD=bytes([0x8b]),
    OP_1SUB=bytes([0x8c]),
    OP_2MUL=bytes([0x8d]),  # disabled
    OP_2DIV=bytes([0x8e]),  # disabled
    OP_NEGATE=bytes([0x8f]),
    OP_ABS=bytes([0x90]),
    OP_NOT=bytes([0x91]),
    OP_0NOTEQUAL=bytes([0x92]),
    OP_ADD=bytes([0x93]),
    OP_SUB=bytes([0x94]),
    OP_MUL=bytes([0x95]),  # disabled
    OP_DIV=bytes([0x96]),  # disabled
    OP_MOD=bytes([0x97]),  # disabled
    OP_LSHIFT=bytes([0x98]),  # disabled
    OP_RSHIFT=bytes([0x99]),   # disabled
    OP_BOOLAND=bytes([0x9a]),
    OP_BOOLOR=bytes([0x9b]),
    OP_NUMEQUAL=bytes([0x9c]),
    OP_NUMEQUALVERIFY=bytes([0x9d]),
    OP_NUMNOTEQUAL=bytes([0x9e]),
    OP_LESSTHAN=bytes([0x9f]),
    OP_GREATERTHAN=bytes([0xa0]),
    OP_LESSTHANOREQUAL=bytes([0xa1]),
    OP_GREATERTHANOREQUAL=bytes([0xa2]),
    OP_MIN=bytes([0xa3]),
    OP_MAX=bytes([0xa4]),
    OP_WITHIN=bytes([0xa5]),
))
# Crypto
CROPTO = EnumDict(dict(
    OP_RIPEMD160=bytes([0xa6]),
    OP_SHA1=bytes([0xa7]),
    OP_SHA256=bytes([0xa8]),
    OP_HASH160=bytes([0xa9]),
    OP_HASH256=bytes([0xaa]),
    OP_CODESEPARATOR=bytes([0xab]),
    OP_CHECKSIG=bytes([0xac]),
    OP_CHECKSIGVERIFY=bytes([0xad]),
    OP_CHECKMULTISIG=bytes([0xae]),
    OP_CHECKMULTISIGVERIFY=bytes([0xaf]),
))

# Locktime

LOCKTIME = EnumDict(dict(
    OP_CHECKLOCKTIMEVERIFY=bytes([0xb1]),
    OP_CHECKSEQUENCEVERIFY=bytes([0xb2]),
))

# Pesu-words
PESU_WORDS = EnumDict(dict(
# These words are used internally for assisting with transaction matching. They are invalid if used in actual scripts.  # noqa
    OP_PUBKEYHASH=bytes([0xfd]),
    OP_PUBKEY=bytes([0xfe]),
    OP_INVALIDOPCODE=bytes([0xff]),
))
# Reserved words
RESERVED_WORDS = EnumDict(dict(
    # Any opcode not assigned is also reserved. Using an unassigned opcode makes the transaction invalid. # no qa
    OP_PERSERVED=bytes([0x50]),
    OP_VER=bytes([0x62]),
    OP_VERIF=bytes([0x65]),
    OP_VERNOTIF=bytes([0x66]),
    OP_RESERVED1=bytes([0x89]),
    OP_RESERVED2=bytes([0x8a]),

    OP_NOP1=bytes([0xb0]),
    OP_NOP4=bytes([0xb3]),
    OP_NOP5=bytes([0xb4]),
    OP_NOP6=bytes([0xb5]),
    OP_NOP7=bytes([0xb6]),
    OP_NOP8=bytes([0xb7]),
    OP_NOP9=bytes([0xb8]),
    OP_NOP10=bytes([0xb9]),
))


OPS = reduce(add, [
    RESERVED_WORDS,
    PESU_WORDS,
    LOCKTIME,
    CROPTO,
    ARITHMETIC,
    BITWISE_LOGIC,
    STACK,
    FLOW_CONTROL,
    CONSTS,
    SPLICE
])

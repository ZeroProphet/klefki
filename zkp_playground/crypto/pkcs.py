import hashlib
from zkp_playground.utils import parse_lv_format
# https://medium.com/@bn121rajesh/rsa-sign-and-verify-using-openssl-behind-the-scene-bf3cac0aade2

"""
For the six hash functions mentioned in Appendix B.1, the DER
encoding T of the DigestInfo value is equal to the following:

MD2:     (0x)30 20 30 0c 06 08 2a 86 48 86 f7 0d 02 02 05 00 04
               10 || H.
MD5:     (0x)30 20 30 0c 06 08 2a 86 48 86 f7 0d 02 05 05 00 04
               10 || H.
SHA-1:   (0x)30 21 30 09 06 05 2b 0e 03 02 1a 05 00 04 14 || H.
SHA-256: (0x)30 31 30 0d 06 09 60 86 48 01 65 03 04 02 01 05 00
               04 20 || H.
SHA-384: (0x)30 41 30 0d 06 09 60 86 48 01 65 03 04 02 02 05 00
               04 30 || H.
SHA-512: (0x)30 51 30 0d 06 09 60 86 48 01 65 03 04 02 03 05 00
                  04 40 || H.
"""

SHA1 = "3021300906052b0e03021a05000414"
SHA256 = "3031300d060960864801650304020105000420"


def gen_pad(n, msg, hash_type):
    key_len = len(hex(n)) - 2
    if hash_type == "SHA1":
        m = SHA1
        h = hashlib.sha1(msg.encode()).hexdigest()
    elif hash_type == "SHA256":
        m = SHA256
        h = hashlib.sha256(msg.encode()).hexdigest()
    else:
        raise Exception(
            "Im too lazy to add all the hash type support, please open a pull requrest if you like")
    pad = "f" * (key_len - len(h) - len(m) - 4 - 2)
    return "0001" + pad + "00" + m + h

import sys
from klefki.blockchain import bitcoin, eos, ethereum


# klefki.bitcoin/eos/ethereum was mv to klefki.blockchain
sys.modules['klefki.bitcoin'] = bitcoin
sys.modules['klefki.eos'] = eos
sys.modules['klefki.ethereum'] = ethereum

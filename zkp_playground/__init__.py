import sys
from zkp_playground.blockchain import bitcoin, eos, ethereum


# zkp_playground.bitcoin/eos/ethereum was mv to zkp_playground.blockchain
sys.modules['zkp_playground.bitcoin'] = bitcoin
sys.modules['zkp_playground.eos'] = eos
sys.modules['zkp_playground.ethereum'] = ethereum

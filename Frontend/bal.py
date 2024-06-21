from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair

# Creates an instance of account which is already deployed
# Account using transaction version=1 (has __validate__ function)
client = FullNodeClient(node_url="your.node.url")
account = Account(
    client=client,
    address="0x4321",
    key_pair=KeyPair(private_key=654, public_key=321),
    chain=StarknetChainId.SEPOLIA,
)


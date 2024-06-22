from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.contract import Contract
from ABIs.dmail import DMAIL_TRANSACTION_ABI



async def dmail_send_email(account):
    contract = Contract(
        address='0x0454F0BD015E730E5ADBB4F080B075FDBF55654FF41EE336203AA2E1AC4D4309',
        abi=DMAIL_TRANSACTION_ABI,
        provider=account,
    )

    _email = f"{account}@dmail.ai".encode()
    _message = "Pipeline inserted".encode()

    invocation = await contract.functions["transaction"].invoke(
        _email.hex(), _message.hex(), auto_estimate=True
    )

    await invocation.wait_for_acceptance()
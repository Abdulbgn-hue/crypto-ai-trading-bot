import os

from web3 import Web3


RPC_URL = os.getenv("EVM_RPC_URL")
PRIVATE_KEY = os.getenv("EVM_PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")


def get_web3():
    if not RPC_URL:
        raise RuntimeError(
            "EVM_RPC_URL is not configured."
        )

    web3 = Web3(
        Web3.HTTPProvider(RPC_URL)
    )

    if not web3.is_connected():
        raise RuntimeError(
            "Could not connect to EVM RPC."
        )

    return web3


def get_wallet_address():

    if not WALLET_ADDRESS:
        raise RuntimeError(
            "WALLET_ADDRESS is not configured."
        )

    return Web3.to_checksum_address(
        WALLET_ADDRESS
    )


def get_balance():

    web3 = get_web3()
    address = get_wallet_address()

    balance = web3.eth.get_balance(
        address
    )

    return {
        "address": address,
        "balance_wei": balance,
        "balance_native": float(
            web3.from_wei(
                balance,
                "ether",
            )
        ),
    }


def sign_transaction(transaction: dict):

    if not PRIVATE_KEY:
        raise RuntimeError(
            "EVM_PRIVATE_KEY is not configured."
        )

    web3 = get_web3()

    signed = web3.eth.account.sign_transaction(
        transaction,
        PRIVATE_KEY,
    )

    return signed


def send_signed_transaction(
    transaction: dict,
):

    web3 = get_web3()

    signed = sign_transaction(
        transaction
    )

    tx_hash = web3.eth.send_raw_transaction(
        signed.raw_transaction
    )

    return {
        "success": True,
        "tx_hash": tx_hash.hex(),
  }

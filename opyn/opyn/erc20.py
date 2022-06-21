#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Anil@Opyn
# Created Date: 06/08/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module to interact with ERC20 contracts """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from opyn.contract import ContractConnection
from opyn.definitions import ContractConfig
from opyn.utils import get_address

# ---------------------------------------------------------------------------
# ERC20 Contract
# ---------------------------------------------------------------------------
class ERC20Contract(ContractConnection):
    """
    Object to create connection to an ERC20 contract

    Args:
        config (ContractConfig): Configuration to setup the Contract
    """
    abi_location = "abis/ERC20.json"

    def __init__(self, config: ContractConfig):
        super().__init__(config)
        self.name = self.contract.functions.name().call()
        self.symbol = self.contract.functions.symbol().call()
        self.decimals = self.contract.functions.decimals().call()

    def get_allowance(self, owner: str, spender: str) -> int:
        """
        Method to get allowance of owner

        Args:
            owner (str): Address of owner's address e.g. user wallet address
            spender (str): Address of spender's address e.g. the Swap contract

        Raises:
            ValueError: Address of wallet is invalid

        Returns:
            allowance (int): Amount owner approved for spender to use
        """
        owner_address = get_address(owner)
        spender_address = get_address(spender)

        response = self.contract.functions.allowance(
            owner_address, spender_address
        ).call()

        return response

    def get_balance(self, owner: str) -> int:
        """
        Method to get balance of owner

        Args:
            owner (str): Address of owner's address e.g. user wallet address

        Raises:
            ValueError: Address of wallet is invalid

        Returns:
            balance (int): Owner's balance
        """
        owner_address = get_address(owner)

        response = self.contract.functions.balanceOf(owner_address).call()

        return response

    def approve(self, publicKey: str, privateKey: str, spender: str, amount: str):
        nonce = self.w3.eth.get_transaction_count(publicKey) 
        tx = self.contract.functions.approve(get_address(spender), amount) \
            .buildTransaction({
                "nonce": nonce
            })

        signed_tx = self.w3.eth.account \
            .sign_transaction(tx, private_key=privateKey)

        self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        self.w3.eth.wait_for_transaction_receipt(signed_tx.hash, timeout=600)

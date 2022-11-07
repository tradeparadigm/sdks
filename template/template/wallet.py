""" Module for wallet utilities """
from template.definitions import Bid, ContractConfig


class Wallet:
    """
    Object to generate bid signature

    Args:
        public_key (str): Public key of the user
                          in hex format with 0x prefix
        private_key (str): Private key of the user
                           in hex format with 0x prefix

    Attributes:
        signer (object): Instance of signer to generate signature
    """

    def __init__(self, public_key: str | None = None, private_key: str | None = None):
        if not private_key and not public_key:
            raise ValueError("Can't instanciate a Wallet without a public or private key")
        ...

    def verify_allowance(self, swap_config: ContractConfig, token_address: str) -> bool:
        """Verify wallet's allowance for a given token

        Args:
            config (ContractConfig): Configuration to setup
                                    the Swap Contract
            token_address (str): Address of token

        Returns:
            verified (bool): True if wallet has sufficient allowance
        """

        return True

    def sign_bid(self, bid: Bid) -> str:
        return "your-signature"

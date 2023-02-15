""" Module for wallet utilities """
import eth_keys  # type: ignore
import web3
from eth_abi.packed import encode_abi_packed
from eth_account.messages import encode_defunct
from web3 import Web3

from thetanuts.definitions import Bid


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

    def __init__(self, public_key: str = "", private_key: str = ""):
        if private_key == "" and public_key == "":
            raise ValueError("Can't instanciate a Wallet without a public or private key")

        self.private_key = private_key
        self.public_key = public_key

        if self.private_key:
            self.signer = eth_keys.keys.PrivateKey(bytes.fromhex(self.private_key[2:]))
            if not self.public_key:
                self.public_key = Web3.toChecksumAddress(self.signer.public_key.to_address())

    def sign_msg(self, messageHash: str) -> str:
        """Sign a hash message using the signer object
        Args:
            messageHash (str): Message to be signed
                               in hex format with 0x prefix
        Returns:
            signature (dict): returns Signature in hex string
        """
        return str(self.signer.sign_message(bytes.fromhex(messageHash[2:])).to_hex())

    def sign_bid(self, bid: Bid) -> str:
        """Sign a bid
        Args:
            bid (dict): Dicionary of bid specification
        Raises:
            TypeError: Bid argument is not an instance of Bid class
        Returns:
            signature (str): Signature of bid
        """
        if not isinstance(bid, Bid):
            raise TypeError("Invalid bid")

        if not self.private_key:
            raise ValueError("Unable to sign. Create the Wallet with the private key argument.")

        signerWallet = Web3.toChecksumAddress(bid.signerWallet)

        if signerWallet != self.public_key:
            raise ValueError("Signer wallet address mismatch")

        toSign = encode_abi_packed(
            ['address', 'uint', 'uint', 'address'],
            [
                bid.vaultAddress,
                bid.nonce,
                int(bid.sellAmount),
                signerWallet,
            ],
        )
        print(
            "Wallet signing bid",
            [
                bid.vaultAddress,
                bid.nonce,
                int(bid.sellAmount),
                signerWallet,
            ],
        )
        signature = web3.eth.Eth.account.sign_message(
            encode_defunct(web3.Web3.keccak(toSign)), private_key=self.signer.to_hex()
        ).signature.hex()

        return str(signature)

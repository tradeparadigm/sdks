from anchorpy import Wallet
from friktion_swap_client.offer import Offer
from numpy import rec
from solana.publickey import PublicKey
import sys
sys.path.insert(0, "/Users/alexwlezien/Friktion/paradigm-integration/friktion-anchor")
from .friktion_anchor.accounts import SwapOrder, UserOrders
from .friktion_anchor.program_id import PROGRAM_ID
from .friktion_anchor.instructions import create
from solana.rpc.async_api import AsyncClient
from .constants import WHITELIST_TOKEN_MINT

class SwapOrderTemplate():

    options_contract_key: PublicKey

    give_size: int
    receive_size: int
    expiry: int
    is_counterparty_provided: bool
    is_whitelisted: bool
    
    give_mint: PublicKey
    receive_mint: PublicKey

    creator_give_pool: PublicKey
    counterparty: PublicKey
    whitelist_token_mint: PublicKey

    def __init__(self, options_contract_key: PublicKey, give_size: int, receive_size: int, 
                expiry: int, give_mint: PublicKey,
                receive_mint: PublicKey, creator_give_pool: PublicKey,
                counterparty: PublicKey,
                is_counterparty_provided: bool = True, 
                is_whitelisted: bool = False,
                whitelist_token_mint: PublicKey = WHITELIST_TOKEN_MINT
        ):
        self.options_contract_key = options_contract_key
        self.give_size = give_size
        self.receive_size = receive_size
        self.expiry = expiry
        self.is_counterparty_provided = is_counterparty_provided
        self.is_whitelisted = is_whitelisted

        self.give_mint = give_mint
        self.receive_mint = receive_mint
        self.creator_give_pool = creator_give_pool
        self.counterparty = counterparty
        self.whitelist_token_mint = whitelist_token_mint

    def as_offer(self) -> Offer:
        return Offer(
            self.give_mint,
            self.receive_mint,
            self.give_size,
            0,
            self.give_size
        )

    @staticmethod
    def from_offer(
        offer: Offer,
        options_contract: PublicKey,
        # placeholder: can be any number, will be deprecated soon
        receive_amount: int,
        expiry: int, 
        creator_give_pool: PublicKey,
        counterparty: PublicKey,
        is_counterparty_provided: bool = True, 
        is_whitelisted: bool = False,
        whitelist_token_mint: PublicKey = WHITELIST_TOKEN_MINT
    ):
        return SwapOrderTemplate(
            options_contract,
            offer.offerAmount,
            receive_amount,
            expiry,
            offer.oToken,
            offer.biddingToken,
            creator_give_pool,
            counterparty,
            is_counterparty_provided,
            is_whitelisted,
            whitelist_token_mint
        )
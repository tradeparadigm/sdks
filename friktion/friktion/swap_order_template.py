import sys

from solana.publickey import PublicKey

from friktion.constants import WHITELIST_TOKEN_MINT
from friktion.offer import Offer

sys.path.insert(0, "/Users/alexwlezien/Friktion/paradigm-integration/friktion-anchor")


class SwapOrderTemplate:

    options_contract_key: PublicKey

    creator: PublicKey

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

    def __init__(
        self,
        creator: PublicKey,
        options_contract_key: PublicKey,
        give_size: int,
        receive_size: int,
        expiry: int,
        give_mint: PublicKey,
        receive_mint: PublicKey,
        creator_give_pool: PublicKey,
        counterparty: PublicKey,
        is_counterparty_provided: bool = True,
        is_whitelisted: bool = False,
        whitelist_token_mint: PublicKey = WHITELIST_TOKEN_MINT,
    ):
        self.creator = creator
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
            oToken=self.give_mint,
            biddingToken=self.receive_mint,
            expiry=self.expiry,
            offerAmount=self.give_size,
            minPrice=0,
            minBidSize=self.give_size,
            seller=self.creator,
        )

    @staticmethod
    def from_offer(
        offer: Offer,
        options_contract: PublicKey,
        # placeholder: can be any number, will be deprecated soon
        receive_amount: int,
        creator_give_pool: PublicKey,
        counterparty: PublicKey,
        is_counterparty_provided: bool = True,
        is_whitelisted: bool = False,
        whitelist_token_mint: PublicKey = WHITELIST_TOKEN_MINT,
    ):
        return SwapOrderTemplate(
            offer.seller,
            options_contract,
            offer.offerAmount,
            receive_amount,
            offer.expiry,
            offer.oToken,
            offer.biddingToken,
            creator_give_pool,
            counterparty,
            is_counterparty_provided,
            is_whitelisted,
            whitelist_token_mint,
        )

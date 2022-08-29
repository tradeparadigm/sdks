# ---------------------------------------------------------------------------
""" Module to call oToken contract """
# ---------------------------------------------------------------------------
from sdk_commons.config import OfferTokenDetails
from template.definitions import ContractConfig


class oTokenContract:
    """
    Object to create connection to the an oToken contract

    Args:
        config (ContractConfig): Configuration to setup the Contract
    """

    def __init__(self, config: ContractConfig):
        ...

    def get_otoken_details(self) -> OfferTokenDetails:
        """
        Method to validate bid

        Args:

        Returns:
            response (dict): Dictionary oToken details
        """

        return {
            "collateralAsset": "...",
            "underlyingAsset": "...",
            "strikeAsset": "...",
            "strikePrice": 0.0,
            "expiryTimestamp": 0,
            "isPut": True,
        }

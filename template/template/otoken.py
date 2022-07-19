# ---------------------------------------------------------------------------
""" Module to call oToken contract """
# ---------------------------------------------------------------------------

from template.definitions import ContractConfig


class oTokenContract:
    """
    Object to create connection to the an oToken contract

    Args:
        config (ContractConfig): Configuration to setup the Contract
    """

    def __init__(self, config: ContractConfig):
        ...

    def get_otoken_details(self) -> dict:
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
            "strikePrice": "...",
            "expiryTimestamp": "...",
            "isPut": "...",
        }

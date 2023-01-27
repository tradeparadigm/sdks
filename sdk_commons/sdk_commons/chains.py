from enum import Enum, EnumMeta


class MembershipTestEnumMeta(EnumMeta):
    """
    With this you can do membership tests
    e.g. >>> element in YourEnumClass
    """

    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class Chains(Enum, metaclass=MembershipTestEnumMeta):
    ETHEREUM = 1
    ROPSTEN = 3
    # Temporarly disable because not supported yet our side
    # GOERLI = 5
    KOVAN = 42
    AVALANCHE = 43114
    FUJI = 43113
    SOLANA_DEV = 777777
    SOLANA_MAIN = 888888
    MATIC = 137

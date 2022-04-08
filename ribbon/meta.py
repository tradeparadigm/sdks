from enum import Enum, EnumMeta


class MembershipTestEnumMeta(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BaseEnum(Enum, metaclass=MembershipTestEnumMeta):
    """With this you can do membership tests,
    e.g. >>> element in YourEnumClass"""

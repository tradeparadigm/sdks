#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Anil@Opyn
# Created Date: 06/08/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module to store Enum class """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from enum import Enum, EnumMeta

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Steven@Ribbon
# Created Date: 04/04/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module to encode message """
# ---------------------------------------------------------------------------

import re
from typing import Any, Callable, Optional, cast

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from web3 import Web3

from ribbon.utils import encode_type, get_address, hex_concat, hex_pad_right, hex_zero_pad, id

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DOMAIN_FIELD_NAMES = ['name', 'version', 'chainId', 'verifyingContract', 'salt']
DOMAIN_FIELD_TYPES = {
    'name': 'string',
    'version': 'string',
    'chainId': 'uint256',
    'verifyingContract': 'address',
    'salt': 'bytes32',
}

HEX_TRUE = hex_zero_pad(Web3.toHex(1), 32)
HEX_FALSE = hex_zero_pad(Web3.toHex(0), 32)
ADDRESS_ZERO = hex_zero_pad(Web3.toHex(0), 20)

# TODO: to be improved by replacing Any with specific types
EncoderType = Callable[[Any], str]


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------
def uint_encoder(data_type: str) -> EncoderType:
    """
    Encoder for uint types

    Args:
        data_type (str): Data type in string

    Returns:
        encoder (EncoderType): Uint encoder
    """
    match = re.findall('^(u?)int(\d*)$', data_type).pop()
    signed = match[1] == ''
    width = int(match[2]) if len(match) == 3 else 256

    if width % 8 != 0 or width > 256 or (len(match) == 3 and match[2] != str(width)):
        raise ValueError(f'Invalid numeric width: {data_type}')

    boundsUpper = 2 ** (width - 1) - 1 if signed else 2 ** (width) - 1
    boundsLower = -boundsUpper - 1
    return cast(
        EncoderType,
        (
            lambda value: hex_zero_pad(Web3.toHex(int(value)), 32)
            if int(value) < boundsUpper and int(value) > boundsLower
            # TODO this is a return ValueError and not a raise,
            # it is expected? (Please note that exception can't
            # be directly raised from lambdas)
            else ValueError('Value out of bounds')
        ),
    )


def bytes_encoder(data_type: str) -> EncoderType:
    """
    Encoder for bytes types

    Args:
        data_type (str): Data type in string

    Returns:
        encoder (EncoderType): Bytes encoder
    """
    match = re.findall('^bytes(\d+)$', data_type).pop()
    width = int(match[1])

    if width == 0 or width > 32 or match[1] != str(width):
        raise ValueError(f'Invalid bytes width: {data_type}')

    return cast(
        EncoderType,
        (
            lambda value: hex_pad_right(value)
            if len(value) == width
            # TODO this is a return ValueError and not a raise,
            # it is expected? (Please note that exception can't
            # be directly raised from lambdas)
            else ValueError('Invalid bytes length')
        ),
    )


def get_base_encoder(data_type: str) -> Optional[EncoderType]:
    """
    Get the encoder for base types

    Args:
        data_type (str): Data type in string

    Returns:
        encoder (EncoderType): Encoder
    """
    if re.match('^(u?)int(\d*)$', data_type):
        return uint_encoder(data_type)
    elif re.match('^bytes(\d+)$', data_type):
        return bytes_encoder(data_type)
    elif data_type == 'address':
        return lambda value: hex_zero_pad(get_address(value), 32)
    elif data_type == 'bool':
        return lambda value: HEX_TRUE if value else HEX_FALSE
    elif data_type == 'bytes':
        return lambda value: Web3.keccak(text=value).hex()
    elif data_type == 'string':
        return lambda value: id(value)
    else:
        return None


class TypedDataEncoder:
    """
    Object to encode typed data

    Args:
        types (dict): Dictionary of data types

    Attributes:
        types (dict): Instance of signer to generate signature
        _encoderCache (dict): Dictionary to cache encoder
        _types (dict): Dictionary to cache struct names
        links (dict): Dictionary to store links between structs
        parents (dict): Dictionary to store parent of structs
        subtypes (dict): Dictionary to check circular reference
        primaryType (dict): Primary type to encode
    """

    def __init__(self, types: dict) -> None:
        self.types = types
        self._encoderCache: dict[str, EncoderType] = {}
        self._types = {}
        self.links: dict[str, dict[str, bool]] = {}
        self.parents: dict[str, list[str]] = {}
        self.subtypes: dict[str, dict[str, bool]] = {}

        for name in types:

            self.links.setdefault(name, {})
            self.parents.setdefault(name, [])
            self.subtypes.setdefault(name, {})

            uniqueNames = {}

            for field in types[name]:
                fieldName = field['name']

                if fieldName in uniqueNames:
                    raise ValueError(f'Duplicate variable name {fieldName} in {name}')

                uniqueNames[fieldName] = True

                baseType = re.sub('\[[^()]*\]', '', field['type'])

                if baseType == name:
                    raise ValueError(f'Circular type reference: {baseType}')

                encoder = get_base_encoder(baseType)

                if encoder:
                    continue

                self.parents[baseType].append(name)
                self.links[name][baseType] = True

        primaryTypes = [t for t in self.parents if len(self.parents[t]) == 0]

        if len(primaryTypes) == 0:
            raise ValueError('Missing primary type')
        elif len(primaryTypes) > 1:
            raise ValueError('Ambiguous primary types or unused types')

        self.primaryType = primaryTypes[0]

        def checkCircular(data_type: str, found: dict):
            if data_type in found:
                raise ValueError(f'Circular type reference to {data_type}')

            found[data_type] = True

            for child in self.links[data_type]:
                if child not in self.parents:
                    checkCircular(child, found)

                    for subtype in found:
                        self.subtypes[subtype][child] = True

            del found[data_type]

        checkCircular(self.primaryType, {})

        for name in self.subtypes:
            st = sorted(self.subtypes[name].keys())
            self._types[name] = encode_type(name, types[name]) + ''.join(
                [encode_type(t, types[t]) for t in st]
            )

    def _get_encoder(self, data_type: str) -> Optional[EncoderType]:
        """
        Get the encoder for a given type

        Args:
            data_type (str): Data type in string

        Returns:
            encoder (EncoderType): Encoder
        """
        if encoder := get_base_encoder(data_type):
            return encoder

        match = re.findall('\[[^()]*\]', data_type)
        if len(match) > 0:
            match = data_type[:-1].split('[')
            subtype = match[0]
            subEncoder = self.get_encoder(subtype)
            length = 0 if len(match) == 1 else int(match[1])
            # print(length)
            return cast(
                EncoderType,
                (
                    lambda values: Web3.keccak(
                        text=hex_concat(
                            [Web3.keccak(text=subEncoder(value)) for value in values]
                            if subtype in self._types
                            else [subEncoder(value) for value in values]
                        )
                    ).hex()
                    if length >= 0 and len(values) == length
                    # TODO this is a return ValueError and not a raise,
                    # it is expected? (Please note that exception can't
                    # be directly raised from lambdas)
                    else ValueError('Array length mismatched')
                ),
            )

        fields = self.types[data_type]
        if fields is not None:
            encodedType = id(self._types[data_type])
            return lambda value: hex_concat(
                [encodedType]
                + [
                    self.get_encoder(field['type'])(value[field['name']])
                    if field['type'] not in self._types
                    else Web3.keccak(
                        text=self.get_encoder(field['type'])(value[field['name']])
                    ).hex()
                    for field in fields
                ]
            )

        return None

    def get_encoder(self, data_type: str) -> EncoderType:
        """
        Get the base encoder for a given type and store it in cache

        Args:
            data_type (str): Data type in string

        Returns:
            encoder (EncoderType): Encoder
        """
        if data_type in self._encoderCache:
            return self._encoderCache[data_type]
        encoder = self._get_encoder(data_type)

        if not encoder:
            raise ValueError(f"Can't find an encoder function for {data_type} type")

        return encoder

    def encode_data(self, data_type: str, value: dict) -> str:
        """
        Encode the value of a given type

        Args:
            data_type (str): Data type in string
            value (dict): Values corresponding to the type

        Returns:
            data (str): Encoded data
        """
        return self.get_encoder(data_type)(value)

    def hash_struct(self, name: str, value: dict) -> str:
        """
        Generate the hash of encoded data given a type and value

        Args:
            name (str): Data type in string
            value (dict): Values corresponding to the type

        Returns:
            hash (str): Hash of encoded data
        """
        return Web3.keccak(hexstr=self.encode_data(name, value)).hex()

    def hash(self, value: dict) -> str:
        """
        Generate the hash of encoded data for the primary type
        of the given a value

        Args:
            value (dict): Values corresponding to the primary type

        Returns:
            hash (str): Hash of encoded data
        """
        return self.hash_struct(self.primaryType, value)

    @staticmethod
    def _from(types: dict) -> 'TypedDataEncoder':
        """
        Create a new instance of TypedDataEncoder for a given types

        Args:
            types (dict): Dictionary of data types

        Returns:
            TypedDataEncoder (str): A new instance of TypedDataEncoder
        """
        return TypedDataEncoder(types)

    @staticmethod
    def _hash_struct(name: str, types: dict, value: dict) -> str:
        """
        Generate the hash of encoded data given a name, types and value

        Args:
            name(str): Data type in string
            types (dict): Dictionary of data types
            value (dict): Values corresponding to the type

        Returns:
            hash (str): Hash of encoded data
        """
        return TypedDataEncoder._from(types).hash_struct(name, value)

    @staticmethod
    def hash_domain(domain: dict) -> str:
        """
        Encode the domain dictionary

        Args:
            domain (dict): Domain values in dictionary

        Returns:
            hash (str): Hash of encoded domain data
        """
        domainFields = []
        for name in domain:
            if name not in DOMAIN_FIELD_NAMES:
                raise ValueError('Invalid domain key')

            domainFields.append({'name': name, 'type': DOMAIN_FIELD_TYPES[name]})

        domainFields.sort(key=lambda x: DOMAIN_FIELD_NAMES.index(x['name']))

        return TypedDataEncoder._hash_struct(
            'EIP712Domain', {'EIP712Domain': domainFields}, domain
        )

    @staticmethod
    def encode(domain: dict, types: dict, value: dict) -> str:
        """
        Encode a message

        Args:
            domain (dict): Domain values in dictionary
            types (dict): Dictionary of data types
            value (dict): Values corresponding to the types

        Returns:
            data (str): Encoded message
        """
        return hex_concat(
            [
                '0x1901',
                TypedDataEncoder.hash_domain(domain),
                TypedDataEncoder._from(types).hash(value),
            ]
        )

    @staticmethod
    def _hash(domain: dict, types: dict, value: dict) -> str:
        """
        Generate a hash of a message following the EIP712 convention:
        https://eips.ethereum.org/EIPS/eip-712

        Args:
            domain (dict): Domain values in dictionary
            types (dict): Dictionary of data types
            value (dict): Values corresponding to the types

        Returns:
            hash (str): Hash of message
        """
        return Web3.keccak(hexstr=TypedDataEncoder.encode(domain, types, value)).hex()

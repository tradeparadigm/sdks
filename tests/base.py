from enum import Enum
from importlib import import_module
from inspect import Parameter, signature

from sdk_commons.config import SDKConfig


class VenuePackages(Enum):
    TEMPLATE = 'template'
    RIBBON = 'ribbon'
    FRIKTION = 'friktion'
    OPYN = 'opyn'


VENUES = [
    VenuePackages.TEMPLATE.value,
    VenuePackages.RIBBON.value,
    VenuePackages.FRIKTION.value,
    VenuePackages.OPYN.value,
]


class TestsBase:
    def setUp(self):
        pass

    @staticmethod
    def import_module(*args: str) -> str:
        return import_module(".".join(args))

    @staticmethod
    def import_class(*args: str) -> str:
        module = import_module(".".join(args[0:-1]))
        cls_name = args[-1]
        assert hasattr(module, cls_name), f"{'.'.join(args)} not found"

        c = getattr(module, cls_name)
        assert c is not None

        return c

    def get_config_class(self, venue: str):
        """
        Scan the venue.config module to search
        a class inheriting SDKConfig
        """
        module = self.import_module(venue, "config")
        config_class = None

        # Iterate the symbol table
        for name, cls in module.__dict__.items():
            # exclude all elements that are not classes
            if not isinstance(cls, type):
                continue
            # exclude all classes that are from a different module
            # i.e. exclude imported items
            if module.__name__ not in cls.__module__:
                continue

            # exclude all classes not children of SDKConfig
            if not issubclass(cls, SDKConfig):
                continue

            config_class = name
            break

        assert config_class is not None, f"Can't any class inheriting SDKConfig in {venue}.config"

        return config_class

    @staticmethod
    def inspect_method_signature(method: callable, reference: callable):
        """
        These checks are needed because abc
        does no checks on arguments of concrete implementations
        This utility verifies the method signature:
          - all params should correspond to params on the reference
          - additional params with a default value are allowed
          - all methods are expected to accept **kwargs
        """

        method_signature = signature(method).parameters
        reference_signature = signature(reference).parameters

        # Concrete implementations should not accept *args because
        # interface methods are defined to only have named parameters
        assert (
            "args" not in method_signature
        ), f"{method.__module__}.{method.__name__} should not accept *args parameter"

        # Verify that args is exactly *args
        # assert (
        #     method_signature["args"].kind == Parameter.VAR_POSITIONAL
        # ), "wrong args argument, expected *args"

        # All concrete implementations are expected to accept **kwargs
        assert (
            "kwargs" in method_signature
        ), f"{method.__module__}.{method.__name__} is not accepting **kwargs parameter"

        # Verify that kwargs is exactly **kwargs
        assert (
            method_signature["kwargs"].kind == Parameter.VAR_KEYWORD
        ), "wrong kwargs argument, expected **kwargs"

        # Extract from the reference signature all arguments
        # except for args and kwargs
        expected_params = [p for p in reference_signature if p not in ['args', 'kwargs']]

        # Verify if the arguments of the method signature
        # corresponds to the reference signature
        for param_name, method_def in method_signature.items():
            # args and kwargs are already explicitly checked, skipping
            if param_name == "args" or param_name == "kwargs":
                continue
            # Unknown parameters (i.e. parameters not in the reference)
            # are refused, except if they have a default value
            method_path = f"{method.__module__}.{method.__name__}"
            assert (
                param_name in expected_params or method_def.default is not Parameter.empty
            ), f"{method_path} is asking for an unknown parameter {param_name}"

# SDKConfig

This is the abstract common interface that every venues are expected to
implement. Each method will be invoked by Paradigm API by providing all listed
parameters. Each venue is free to include only needed parameters in their own concrete
implementation. All other parameters will be consumed via `**kwargs`.
A template venue is also provided as an example for a concrete implementation.

## Configure your SDK

Each venue can provide its own configuration by inheriting SDKConfig in `your_venue/config.py`.
You are free to name the class as you wish and the only constraints to be followed are:
- the class must be defined in a config.py files into your venue module
- the class must extend SDKConfig

Since SDKConfig is an abstract class you will have to define your implementation of the required methods (e.g. `create_offer`, `get_offer_details`, `verify_allowance`, ...) and properties like (e.g. `authorization_pages`, `supported_chains`, ...)
You will find the full list of abstract methods and properties in [SDKConfig](https://github.com/tradeparadigm/sdks/blob/improved-docs/sdk_commons/sdk_commons/config.py)

Please note that every method is expected to receive a predefined list of parameters and it is expected to return a specific output value.
Your own implementation can include all or some of the expected parameters (some of them could be specific for other partners and you are free to ignore them). Each method is expected to include a `**kwargs` parameter to consume all remaining parameters that you want to ignore in your implementation.
You should not include additional parameters, but if you strictly need to do that you can introduce additional parameters by assigning them a default value.

You can refer to the [template venue](https://github.com/tradeparadigm/sdks/tree/improved-docs/template/template) implementation as a generic example of integration

### Define your underlying code

As long as you will provide the expected interface, you are free to implement your underlying code at your will.

## Unittests and type checks

To ensure that every SDKs is compliant to the expected interface a set of unittests have been introduced.
These unittests verify the implementation of the interface by also verifying method signatures. No functional tests are executed at the moment, so the tests can't guarantee that the implementation of the interface methods are correctly linked to the underlying code and that the underlying is correctly working.
Unittests will be automatically executed when a PR will be created.

Furthermore type hints will be checked via mypy to ensure type safety and to verify that the return values on the implemented methods match the expected interface.

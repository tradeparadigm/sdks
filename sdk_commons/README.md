# SDKConfig

This is the abstract common interface that every venues are expended to
implement. Each method will be invoked by API providing all listed parameters
but each venue is free to only include needed parameters in their own concrete
implementation. All other parameters will be consumed by *args and **kwargs
that are always expected to be included.
A template venue is also provided as example for a concrete implementation.

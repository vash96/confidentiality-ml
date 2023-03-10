from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Float(_message.Message):
    __slots__ = ["x"]
    X_FIELD_NUMBER: _ClassVar[int]
    x: float
    def __init__(self, x: _Optional[float] = ...) -> None: ...

class NDArray(_message.Message):
    __slots__ = ["data", "shape"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    shape: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, data: _Optional[bytes] = ..., shape: _Optional[_Iterable[int]] = ...) -> None: ...

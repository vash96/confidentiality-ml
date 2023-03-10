import basic_types_pb2 as _basic_types_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

from basic_types_pb2 import Empty
from basic_types_pb2 import Float
from basic_types_pb2 import NDArray
COL: ScrambleKind
DESCRIPTOR: _descriptor.FileDescriptor
ROW: ScrambleKind

class Permutation(_message.Message):
    __slots__ = ["data", "kind"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    kind: ScrambleKind
    def __init__(self, data: _Optional[bytes] = ..., kind: _Optional[_Union[ScrambleKind, str]] = ...) -> None: ...

class Scrambled(_message.Message):
    __slots__ = ["array", "perm"]
    ARRAY_FIELD_NUMBER: _ClassVar[int]
    PERM_FIELD_NUMBER: _ClassVar[int]
    array: _basic_types_pb2.NDArray
    perm: Permutation
    def __init__(self, array: _Optional[_Union[_basic_types_pb2.NDArray, _Mapping]] = ..., perm: _Optional[_Union[Permutation, _Mapping]] = ...) -> None: ...

class ToScramble(_message.Message):
    __slots__ = ["array", "kind"]
    ARRAY_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    array: _basic_types_pb2.NDArray
    kind: ScrambleKind
    def __init__(self, array: _Optional[_Union[_basic_types_pb2.NDArray, _Mapping]] = ..., kind: _Optional[_Union[ScrambleKind, str]] = ...) -> None: ...

class ScrambleKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

from typing import FrozenSet, Union, Tuple
from pathlib import Path
import pickle


# Note bool is a subclass of int
ConstScalarTypes = Union[Path, int, float, str, bytes, None]
ConstTypes = Union[ConstScalarTypes, Tuple[ConstScalarTypes, ...], FrozenSet[ConstScalarTypes]]

CONST_SCALAR_TYPES = (Path, str, bytes, int, float, type(None))


def validate_const_scalar_data(data):
    if not isinstance(data, CONST_SCALAR_TYPES):
        raise TypeError(data)


def validate_const_data(data):
    if isinstance(data, tuple):
        for sub in data:
            validate_const_scalar_data(sub)
    else:
        validate_const_scalar_data(data)


def serialize_const_data(data: ConstTypes) -> bytes:
    return pickle.dumps(data)


def deserialize_const_data(data: bytes) -> ConstTypes:
    return pickle.loads(data)

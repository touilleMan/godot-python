from ._api import get_parent, Isengard
from ._const import ConstTypes
from ._target import (
    BaseTargetHandler,
    FileTargetHandler,
    FolderTargetHandler,
    VirtualTargetHandler,
    DeferredTargetHandler,
)
from ._exceptions import (
    IsengardError,
    IsengardStateError,
    IsengardDefinitionError,
    IsengardConsistencyError,
    IsengardRunError,
)


__all__ = (
    # _api
    "get_parent",
    "Isengard",
    # _const
    "ConstTypes",
    # _target
    "BaseTargetHandler",
    "FileTargetHandler",
    "FolderTargetHandler",
    "VirtualTargetHandler",
    "DeferredTargetHandler",
    # _exceptions
    "IsengardError",
    "IsengardStateError",
    "IsengardDefinitionError",
    "IsengardConsistencyError",
    "IsengardRunError",
    # misc
    "QUOTES",
    "get_parent",
)


QUOTES = [
    "So you've chosen... build.",
    "A build system is a dangerous tool Saruman !",
    "The build is later than you think.",
    "You have elected the way of... build!",
    "All we have to do is decide what to build with the time that is given to us.",
    "There are other build systems at work in this world, Frodo, besides the will of evil.",
    "Do not be too eager to deal out rebuild in judgment.",
    "Build you fools !",
]

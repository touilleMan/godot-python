from ._api import Isengard, get_parent
from ._target import (
    Target,
    VirtualTarget,
    ConfiguredVirtualTarget,
    VirtualTargetResolver,
    FSTarget,
    FileTarget,
    FolderTarget,
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
    "Isengard",
    "get_parent",
    # _target
    "Target",
    "VirtualTarget",
    "ConfiguredVirtualTarget",
    "VirtualTargetResolver",
    "FSTarget",
    "FileTarget",
    "FolderTarget",
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

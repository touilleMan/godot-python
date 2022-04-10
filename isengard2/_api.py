from contextvars import ContextVar
from pathlib import Path
from typing import Dict, List, Sequence, Set, Callable, Union, Optional, Any, Union, TypeVar, Type
import inspect

from ._utils import ConstTypes, validate_const_data
from ._target import (
    Target,
    VirtualTarget,
    FileTarget,
    FolderTarget,
    ConfiguredTarget,
    ConfiguredVirtualTarget,
    VirtualTargetResolver,
    StablePath,
)
from ._rule import Rule, _INPUT_OUTPUT_CONFIG_NAMES
from ._exceptions import (
    IsengardError,
    IsengardStateError,
    IsengardDefinitionError,
    IsengardConsistencyError,
    IsengardRunError,
)


C = TypeVar("C", bound=Callable[..., None])
TargetLike = Union[str, Target]


_RESERVED_CONFIG_NAMES = {
    *_INPUT_OUTPUT_CONFIG_NAMES,
    "rootdir",  # Entrypoint script's directory
    "ruledir",  # Directory of the script the current rule was defined in
}


_parent: ContextVar["Isengard"] = ContextVar("context")


def get_parent() -> "Isengard":
    try:
        return _parent.get()
    except LookupError as exc:
        raise IsengardError("Not in a subdir !") from exc


class Isengard:
    def __init__(
        self,
        self_file: Union[str, Path],
        db: Union[str, Path] = ".isengard.sqlite",
        subdir_default_filename: Optional[str] = None,
    ):
        raise NotImplementedError

    @property
    def rootdir(self):
        raise NotImplementedError

    def register_target_cooker(self, suffix: str, target_cls: Type[Target]):
        raise NotImplementedError

    def subscript(self, subscript: Union[str, Path]) -> None:
        raise NotImplementedError

    def subdir(self, subdir: str, filename: Optional[str] = None) -> None:
        raise NotImplementedError

    def configure(self, **config: ConstTypes):
        """
        Note passing configuration as function arguments limit the name you can use
        (e.g. `compiler.c.flags` is not a valid name). This is intended to work
        well with dependency injection in the rule where configuration is requested
        by using it name as function argument.
        """
        raise NotImplementedError

    def lazy_config(self, fn):
        raise NotImplementedError

    def lazy_rule(self, fn):
        raise NotImplementedError

    def rule(
        self,
        outputs: Optional[Sequence[TargetLike]] = None,
        output: Optional[TargetLike] = None,
        inputs: Optional[Sequence[TargetLike]] = None,
        input: Optional[TargetLike] = None,
        name: Optional[str] = None,
    ) -> Callable[[C], C]:
        raise NotImplementedError

    def run(self, target: Union[TargetLike, Path]) -> None:
        raise NotImplementedError

    def clean(self, target: Union[TargetLike, Path]) -> None:
        raise NotImplementedError

    def list_configured_targets(self) -> Sequence[Union[Path, str]]:
        raise NotImplementedError

    def dump_graph(
        self,
        target: Optional[TargetLike] = None,
        display_configured: bool = False,
        display_relative_path: bool = False,
    ) -> str:
        """
        Graph example:
            a.out#
            ├─rule:link_c
            ├─config:linkflags
            ├─x.o#
            │ ├─rule:compile_c
            │ ├─config:cflags
            │ ├─x.c#
            │ └─headers/
            │   ├─rule:generate_headers
            │   └─config:headers_config
            └─y.o#
              ├─rule:compile_c
              ├─config:cflags
              ├─y.c#
              └─headers/
                ├─rule:generate_headers
                └─…
        """
        raise NotImplementedError

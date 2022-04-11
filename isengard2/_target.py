from typing import Optional, Any, TypeVar, Generic, Tuple, Type, Dict, Sequence, NewType
from pathlib import Path
from struct import pack
from hashlib import sha256
from os import stat
from stat import S_ISDIR
import pickle
from shutil import rmtree

from ._exceptions import IsengardDefinitionError, IsengardConsistencyError, IsengardRunError
from ._const import ConstTypes


# Rules are defined with unresolved target ID (e.g. `{build}/foo.c#`, `bar.log#`)
# that are relative to their rule's workdir and contains config variables.
# Resolution turn them into unique absolute ID (e.g. `/home/x/project/build/foo.c#`,
# `/home/x/project/bar.log#`)
# Note both unresolved and resolved targets must contain a discriminant suffix.
UnresolvedTargetID = NewType('UnresolvedTargetID', str)
ResolvedTargetID = NewType('ResolvedTargetID', str)


class TargetHandlersBundle:
    def __init__(self, target_handlers: Sequence["BaseTargetHandler"], default_handler: Optional["BaseTargetHandler"] =None):
        self.default_handler = default_handler
        handler_per_suffix: Dict[str, BaseTargetHandler] = {}

        for handler in target_handlers:
            if handler.DISCRIMINANT_SUFFIX:
                ambiguous = next((h for h in target_handlers if h.DISCRIMINANT_SUFFIX.endswith(handler.DISCRIMINANT_SUFFIX) and h is not handler), None)
                if ambiguous:
                    raise IsengardConsistencyError(
                        f"Ambiguous target handler suffix `{handler.DISCRIMINANT_SUFFIX}`, would clash between {handler} and {ambiguous}"
                    )
                handler_per_suffix[handler.DISCRIMINANT_SUFFIX] = handler

        self.handler_per_suffix = handler_per_suffix

    def resolve_target(self, target: str, config: Dict[str, ConstTypes], workdir: Path) -> Tuple[ResolvedTargetID, "BaseTargetHandler"]:
        for suffix, handler in self.handler_per_suffix.items():
            if target.endswith(suffix):
                return (handler.resolve(UnresolvedTargetID(target), config, workdir), handler)
        else:
            if self.default_handler:
                patched_target = UnresolvedTargetID(target + self.default_handler.DISCRIMINANT_SUFFIX)
                return (self.default_handler.resolve(patched_target, config, workdir), self.default_handler)
            else:
                raise IsengardConsistencyError(f"No handler for target `{target}` (is discriminant suffix valid ?)")

    def cook_target(self, target: ResolvedTargetID, previous_fingerprint: Optional[bytes]) -> Tuple[Any, "BaseTargetHandler"]:
        for suffix, handler in self.handler_per_suffix.items():
            if target.endswith(suffix):
                return (handler.cook(target, previous_fingerprint), handler)
        else:
            if self.default_handler:
                return (self.default_handler.cook(target, previous_fingerprint), self.default_handler)
            else:
                raise IsengardConsistencyError(f"No handler for target `{target}` (is discriminant suffix valid ?)")


T = TypeVar('T')


class BaseTargetHandler(Generic[T]):
    TARGET_TYPE: Type[T]
    DISCRIMINANT_SUFFIX: str
    # Allow target that exists before any rule is run (i.e. basically the source
    # files by opposition of the generated files and virtual targets)
    ALLOW_NON_RULE_GENERATED_TARGET: bool

    def __repr__(self) -> str:
        return f"{type(self).__name__}(discriminant_suffix={self.DISCRIMINANT_SUFFIX!r}, target_type={self.TARGET_TYPE!r})"

    def resolve(self, id: UnresolvedTargetID, config: Dict[str, ConstTypes], workdir: Path) -> ResolvedTargetID:
        try:
            return ResolvedTargetID(id.format(**config))
        except KeyError as exc:
            raise IsengardDefinitionError(
                f"Missing configuration `{exc.args[0]}` needed in `{id}`"
            )

    def cook(self, id: ResolvedTargetID, previous_fingerprint: Optional[bytes]) -> T:
        raise NotImplementedError

    def clean(self, cooked: T) -> None:
        raise NotImplementedError

    def compute_fingerprint(self, cooked: T) -> Optional[bytes]:
        raise NotImplementedError

    def need_rebuild(self, cooked: T, previous_fingerprint: bytes) -> bool:
        return self.compute_fingerprint(cooked) != previous_fingerprint


class FileTargetHandler(BaseTargetHandler):
    TARGET_TYPE = Path
    DISCRIMINANT_SUFFIX = "#"
    ALLOW_NON_RULE_GENERATED_TARGET = True

    def resolve(self, id: UnresolvedTargetID, config: Dict[str, ConstTypes], workdir: Path) -> ResolvedTargetID:
        resolved = super().resolve(id, config, workdir)
        if resolved:
            # Note `resolved` contains the discriminant suffix, hence `Path(resolved)`
            # doesn't really correspond to the actual cooked path
            if not Path(resolved).is_absolute():
                return ResolvedTargetID(str(workdir / resolved))
        return resolved

    def cook(self, id: ResolvedTargetID, previous_fingerprint: Optional[bytes]) -> Path:
        return Path(id[:-1])

    def clean(self, cooked: Path) -> None:
        try:
            cooked.unlink()
        except FileNotFoundError:
            pass

    def compute_fingerprint(self, cooked: Path) -> Optional[bytes]:
        fingerprint = bytearray(40)  # 8 bytes timestamp + 32 bytes sha256 hash
        try:
            fingerprint[:8] = pack("!d", stat(cooked).st_mtime)
            with open(cooked, "rb") as fd:
                fingerprint[8:] = sha256(fd.read()).digest()
            return fingerprint
        except (FileNotFoundError, IsADirectoryError):
            return None

    def need_rebuild(self, cooked: Path, previous_fingerprint: bytes) -> bool:
        try:
            if previous_fingerprint[:8] != pack("!d", stat(cooked).st_mtime):
                return True
            with open(cooked, "rb") as fd:
                if previous_fingerprint[8:] != sha256(fd.read()).digest():
                    return True
            return False
        except (FileNotFoundError, IsADirectoryError):
            return True


class FolderTargetHandler(BaseTargetHandler):
    TARGET_TYPE = Path
    DISCRIMINANT_SUFFIX = "/"
    ALLOW_NON_RULE_GENERATED_TARGET = True

    def resolve(self, id: UnresolvedTargetID, config: Dict[str, ConstTypes], workdir: Path) -> ResolvedTargetID:
        resolved = super().resolve(id, config, workdir)
        if resolved:
            # Note `resolved` contains the discriminant suffix, hence `Path(resolved)`
            # doesn't really correspond to the actual cooked path
            if not Path(resolved).is_absolute():
                # Discriminant being a `/` is is removed when converting Path back to str
                return ResolvedTargetID(str(workdir / resolved) + "/")
        return resolved

    def cook(self, id: ResolvedTargetID, previous_fingerprint: Optional[bytes]) -> Path:
        return Path(id[:-1])

    def clean(self, cooked: Path) -> None:
        try:
            rmtree(cooked)
        except FileNotFoundError:
            pass

    def compute_fingerprint(self, cooked: Path) -> Optional[bytes]:
        # TODO: recursively check the folder ?
        try:
            id_stats = stat(cooked)
            if not S_ISDIR(id_stats.st_mode):
                return None
            return pack("!d", id_stats.st_mtime)
        except FileNotFoundError:
            return None


class VirtualTargetHandler(BaseTargetHandler):
    """
    Virtual target doesn't exist on disk, hence they must always be build.
    """

    TARGET_TYPE = str
    DISCRIMINANT_SUFFIX = "@"
    ALLOW_NON_RULE_GENERATED_TARGET = False

    def cook(self, id: ResolvedTargetID, previous_fingerprint: Optional[bytes]) -> str:
        return id

    def clean(self, cooked: str) -> None:
        pass

    def compute_fingerprint(self, cooked: str) -> Optional[bytes]:
        return None

    def need_rebuild(self, cooked: str, previous_fingerprint: bytes) -> bool:
        return True


class DeferredTarget:
    __slot__ = ("target", "_resolved")

    def __init__(self, target: Any):
        self.target = target

    def resolve(self, target: Any, handler: BaseTargetHandler) -> None:
        if not isinstance(target, handler.TARGET_TYPE):
            raise IsengardRunError(f"Incorrect type for target, handler expects `{handler.TARGET_TYPE}`")
        if hasattr(self, "_resolved"):
            raise IsengardRunError("Target already resolved !")
        setattr(self, "_resolved", (target, handler))

    @property
    def resolved(self) -> Optional[Tuple[Any, BaseTargetHandler]]:
        return getattr(self, "_resolved", None)


class DeferredTargetHandler(BaseTargetHandler):
    """
    Deferred targets are placeholder that should be resolved by the rule
    producing them as output.
    This is typically useful when generating file/folder whose name is not
    known in advance.

    example:

        from datetime import datetime
        @isg.rule(output="foo?")
        def generate_logfile(output: DeferredTarget, rootdir: Path) -> None:
            # logfile is named something like `2022-04-09T19:50:52.041292.log`
            logfile = rootdir / f"{datetime.now().isoformat()}.log"
            output.resolve(logfile, isengard.FileHandler())
    """

    TARGET_TYPE = DeferredTarget
    DISCRIMINANT_SUFFIX = "?"
    ALLOW_NON_RULE_GENERATED_TARGET = False

    def _load_previous_fingerprint(self, previous_fingerprint: bytes) -> Optional[Tuple[Any, BaseTargetHandler, bytes]]:
        # Resolved target info has been stored in the fingerprint, so cunning !
        try:
            return pickle.loads(previous_fingerprint)
        except Exception:
            # Something wrong occured, we consider the previous fingerprint is
            # no longer compatible with the codebase and hence discard it
            return None

    def cook(self, id: ResolvedTargetID, previous_fingerprint: Optional[bytes]) -> DeferredTarget:
        target = DeferredTarget(id)
        if previous_fingerprint:
            resolved = self._load_previous_fingerprint(previous_fingerprint)
            if resolved:
                resolved_target, resolved_handler, _ = resolved
                target.resolve(resolved_target, resolved_handler)
        return target

    def clean(self, cooked: DeferredTarget) -> None:
        if not cooked.resolved:
            return None
        resolved_target, resolved_handler = cooked.resolved
        resolved_handler.clean(resolved_target)

    def compute_fingerprint(self, cooked: DeferredTarget) -> Optional[bytes]:
        if not cooked.resolved:
            return None

        resolved_target, resolved_handler = cooked.resolved
        resolved_fingerprint = resolved_handler.compute_fingerprint(resolved_target)

        return pickle.dumps((resolved_target, resolved_handler, resolved_fingerprint))

    def need_rebuild(self, cooked: DeferredTarget, previous_fingerprint: bytes) -> bool:
        if not cooked.resolved:
            return True
        resolved_target, resolved_handler = cooked.resolved
        resolved = self._load_previous_fingerprint(previous_fingerprint)
        if not resolved:
            return True
        resolved_previous_fingerprint = resolved[2]
        return resolved_handler.need_rebuild(resolved_target, resolved_previous_fingerprint)

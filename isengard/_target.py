from typing import Optional, Any, TypeVar, Generic, Tuple, Type, Dict, Sequence, NewType
from pathlib import Path
from struct import pack
from hashlib import sha256
from os import stat
from stat import S_ISDIR
import pickle
from shutil import rmtree

from ._exceptions import IsengardConsistencyError, IsengardRunError
from ._const import ConstTypes


# Rules are defined with unresolved target ID (e.g. `{build}/foo.c#`, `bar.log#`)
# that are relative to their rule's workdir and contains config variables.
# Resolution turn them into unique absolute ID (e.g. `/home/x/project/build/foo.c#`,
# `/home/x/project/bar.log#`)
# Note both unresolved and resolved targets must contain a discriminant suffix.
UnresolvedTargetID = NewType("UnresolvedTargetID", str)
ResolvedTargetID = NewType("ResolvedTargetID", str)

# A discriminant suffix is used on unresolved/resolved target to retrieve it
# target handler (which in turn is use to work on the target)
class TargetDiscriminant(str):
    def __new__(cls, raw):
        if len(raw) != 1:
            raise ValueError("Discriminant must be 1 character long !")
        return str.__new__(cls, raw)


# Once resolved, a target is cooked by it target handler, resulting in an arbitrary
# object that will be provided as parameter to the rule function
CookedTarget = NewType("CookedTarget", Any)


class TargetHandlersBundle:
    def __init__(
        self,
        target_handlers: Sequence["BaseTargetHandler"],
        default_target_handler: Optional["BaseTargetHandler"] = None,
    ):
        if default_target_handler and default_target_handler not in target_handlers:
            raise ValueError(
                "`default_target_handler` must be among the values of `target_handlers`"
            )

        self.default_target_handler = default_target_handler
        discriminant_to_handler: Dict[TargetDiscriminant, BaseTargetHandler] = {}

        for handler in target_handlers:
            if handler.DISCRIMINANT:
                ambiguous = next(
                    (
                        h
                        for h in target_handlers
                        if h.DISCRIMINANT.endswith(handler.DISCRIMINANT) and h is not handler
                    ),
                    None,
                )
                if ambiguous:
                    raise IsengardConsistencyError(
                        f"Ambiguous target handler suffix `{handler.DISCRIMINANT}`, would clash between {handler} and {ambiguous}"
                    )
                discriminant_to_handler[handler.DISCRIMINANT] = handler

        self.discriminant_to_handler = discriminant_to_handler

    def resolve_target(
        self, target: str, config: Dict[str, ConstTypes], workdir: Path
    ) -> Tuple[ResolvedTargetID, "BaseTargetHandler"]:
        for suffix, handler in self.discriminant_to_handler.items():
            if target.endswith(suffix):
                return (handler.resolve(UnresolvedTargetID(target), config, workdir), handler)
        else:
            if self.default_target_handler:
                patched_target = UnresolvedTargetID(
                    target + self.default_target_handler.DISCRIMINANT
                )
                return (
                    self.default_target_handler.resolve(patched_target, config, workdir),
                    self.default_target_handler,
                )
            else:
                raise IsengardConsistencyError(
                    f"No handler for target `{target}` (is discriminant suffix valid ?)"
                )

    def get_handler(self, target: ResolvedTargetID) -> "BaseTargetHandler":
        for suffix, handler in self.discriminant_to_handler.items():
            if target.endswith(suffix):
                return handler
        else:
            # In theory we shouldn't reach this point given `target` has been obtained through `get_handler`
            raise IsengardConsistencyError(
                f"No handler for target `{target}` (is discriminant suffix valid ?)"
            )

    def cook_target(
        self, target: ResolvedTargetID, previous_fingerprint: Optional[bytes]
    ) -> Tuple[Any, "BaseTargetHandler"]:
        for suffix, handler in self.discriminant_to_handler.items():
            if target.endswith(suffix):
                return (handler.cook(target, previous_fingerprint), handler)
        else:
            # In theory we shouldn't reach this point given `target` has been obtained through `get_handler`
            raise IsengardConsistencyError(
                f"No handler for target `{target}` (is discriminant suffix valid ?)"
            )


T = TypeVar("T", bound=CookedTarget)


class BaseTargetHandler(Generic[T]):
    COOKED_TYPE: Type[T]
    DISCRIMINANT: TargetDiscriminant
    # Allow target that exists before any rule is run (i.e. basically the source
    # files by opposition of the generated files and virtual targets)
    ON_DISK_TARGET: bool

    def __repr__(self) -> str:
        return f"{type(self).__name__}(discriminant={self.DISCRIMINANT!r}, cooked_type={self.COOKED_TYPE!r})"

    def resolve(
        self, id: UnresolvedTargetID, config: Dict[str, ConstTypes], workdir: Path
    ) -> ResolvedTargetID:
        try:
            return ResolvedTargetID(id.format(**config))
        except KeyError as exc:
            raise IsengardConsistencyError(
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
    COOKED_TYPE = Path
    DISCRIMINANT = TargetDiscriminant("#")
    ON_DISK_TARGET = True

    def __init__(self, fingerprint_strategy: str = "stat+checksum"):
        """
        Fingerprint strategies:
            stat: Use file's st_mtime/st_size/st_mode/st_ino/st_uid/st_gid as fingerprint.
                This strategy is the fastest (only a `os.stat` call is needed) but can
                lead to false negative (i.e. a rule erroneously not being rebuilt) given
                we don't compare the actual content of the file.
                Note `os.stat` work differently depending on the OS/FS (e.g. there is
                no inode on Windows so st_ino correspond to the file index) so we don't
                try to be clever and just consider *any* modification a reason to rebuild.
                See https://apenwarr.ca/log/20181113 for a very cool article on this ;-)

            stat+checksum: Actually compute the sha256 of the file as part of the fingerprint.
                Computing the file hash is much slower that just doing a stat, but prevent
                all false negative.
                Regarding the slowdown part:
                - Hashing is fast, so this should be an issue only on big projects
                - Modern FS keep a cache on recently used files, so the read part of the
                  hash computing should be amortized by the fact the file is going to
                  be read anyway if rebuild is needed
                - On the other hand if rebuild is not needed, the read time is a net lost :(
                  This is a shame given the typical rebuild scenario is having a single
                  file modified in the project...
        """
        self.fingerprint_strategy = fingerprint_strategy
        if fingerprint_strategy not in ("stat", "stat+checksum"):
            raise ValueError('`fingerprint_strategy` value must be "stat" or "stat+checksum"')

    def resolve(
        self, id: UnresolvedTargetID, config: Dict[str, ConstTypes], workdir: Path
    ) -> ResolvedTargetID:
        resolved = super().resolve(id, config, workdir)
        if resolved:
            # Note `resolved` contains the discriminant suffix, hence `Path(resolved)`
            # doesn't really correspond to the actual cooked path
            if not Path(resolved).is_absolute():
                return ResolvedTargetID((workdir / resolved).as_posix())
        return resolved

    def cook(self, id: ResolvedTargetID, previous_fingerprint: Optional[bytes]) -> Path:
        return Path(id[:-1])

    def clean(self, cooked: Path) -> None:
        try:
            cooked.unlink()
            # We let PermissionError&IsADirectoryError goes through given they
            # mark the fact the clean couldn't be performed
        except FileNotFoundError:
            pass

    def compute_fingerprint(self, cooked: Path) -> Optional[bytes]:
        fingerprint = bytearray(
            64
        )  # 32 bytes sha256 stats hash + 32 bytes sha256 file content hash
        try:
            # Trivia: mtime is "modified time", ctime is "change time" (and not
            # "created time") thanks for nothing POSIX naming !
            # But wait there's more ! This is true only for POSIX, on Windows
            # ctime actually contains the created time ^^
            # Long story short: ctime is too messy so we just ignore it
            stats = stat(cooked)
            if S_ISDIR(stats.st_mode):
                return None
            fingerprint[:32] = sha256(
                # Use native byteorder for packing given the fingerprint is not going to be
                # shared with another machine.
                pack(
                    "=dQQQQQ",
                    stats.st_mtime,
                    stats.st_size,
                    stats.st_ino,
                    stats.st_mode,
                    stats.st_uid,
                    stats.st_gid,
                )
            ).digest()
            if self.fingerprint_strategy == "stat+checksum":
                with open(cooked, "rb") as fd:
                    fingerprint[32:] = sha256(fd.read()).digest()

            return fingerprint

        except OSError:
            return None

    def need_rebuild(self, cooked: Path, previous_fingerprint: bytes) -> bool:
        try:
            stats = stat(cooked)
            if S_ISDIR(stats.st_mode):
                return None
            if (
                previous_fingerprint[:32]
                != sha256(
                    pack(
                        "=dQQQQQ",
                        stats.st_mtime,
                        stats.st_size,
                        stats.st_ino,
                        stats.st_mode,
                        stats.st_uid,
                        stats.st_gid,
                    )
                ).digest()
            ):
                return True
            if self.fingerprint_strategy == "stat+checksum":
                with open(cooked, "rb") as fd:
                    if previous_fingerprint[32:] != sha256(fd.read()).digest():
                        return True
            return False

        except OSError:
            return True


class FolderTargetHandler(BaseTargetHandler):
    COOKED_TYPE = Path
    DISCRIMINANT = TargetDiscriminant("/")
    ON_DISK_TARGET = True

    def resolve(
        self, id: UnresolvedTargetID, config: Dict[str, ConstTypes], workdir: Path
    ) -> ResolvedTargetID:
        resolved = super().resolve(id, config, workdir)
        if resolved:
            # Note `resolved` contains the discriminant suffix, hence `Path(resolved)`
            # doesn't really correspond to the actual cooked path
            if not Path(resolved).is_absolute():
                # Discriminant being a `/` is is removed when converting Path back to str
                return ResolvedTargetID((workdir / resolved).as_posix() + "/")
        return resolved

    def cook(self, id: ResolvedTargetID, previous_fingerprint: Optional[bytes]) -> Path:
        return Path(id[:-1])

    def clean(self, cooked: Path) -> None:
        try:
            rmtree(cooked)
            # We let PermissionError&NotADirectoryError goes through given they
            # mark the fact the clean couldn't be performed
        except FileNotFoundError:
            pass

    def compute_fingerprint(self, cooked: Path) -> Optional[bytes]:
        try:
            stats = stat(cooked)
            if not S_ISDIR(stats.st_mode):
                return None
            return sha256(
                # Use native byteorder for packing given the fingerprint is not going to be
                # shared with another machine.
                pack(
                    "=dQQQQQ",
                    stats.st_mtime,
                    stats.st_size,
                    stats.st_ino,
                    stats.st_mode,
                    stats.st_uid,
                    stats.st_gid,
                )
            ).digest()

        except OSError:
            return None


class VirtualTargetHandler(BaseTargetHandler):
    """
    Virtual target doesn't exist on disk, hence they must always be build.
    """

    COOKED_TYPE = str
    DISCRIMINANT = TargetDiscriminant("@")
    ON_DISK_TARGET = False

    def cook(self, id: ResolvedTargetID, previous_fingerprint: Optional[bytes]) -> str:
        return id

    def clean(self, cooked: str) -> None:
        pass

    def compute_fingerprint(self, cooked: str) -> Optional[bytes]:
        return None

    def need_rebuild(self, cooked: str, previous_fingerprint: bytes) -> bool:
        return True


class DeferredTarget(Generic[T]):
    __slot__ = ("id", "_resolved")

    # (<cooked>, <handler>, <previous_fingerprint>)
    _resolved: Tuple[T, BaseTargetHandler, Optional[bytes]]

    def __init__(self, id: ResolvedTargetID, target_handlers_bundle: TargetHandlersBundle):
        self.id = id
        self._target_handlers_bundle = target_handlers_bundle

    def resolve(
        self,
        resolved: T,
        discriminant: TargetDiscriminant,
        _previous_fingerprint: Optional[bytes] = None,
    ) -> None:
        try:
            handler = self._target_handlers_bundle.discriminant_to_handler[discriminant]
        except KeyError:
            raise IsengardRunError(
                f"Incorrect discriminant `{discriminant}`, valid options are: {', '.join(self._target_handlers_bundle.discriminant_to_handler.keys())}"
            )

        if not isinstance(resolved, handler.COOKED_TYPE):
            raise IsengardRunError(
                f"Incorrect resolved type, discriminant expects `{handler.COOKED_TYPE}`"
            )

        if hasattr(self, "_resolved"):
            raise IsengardRunError("Target already resolved !")
        setattr(self, "_resolved", (resolved, handler, _previous_fingerprint))

    @property
    def resolved(self) -> Optional[Tuple[T, BaseTargetHandler]]:
        try:
            return getattr(self, "_resolved")[0]
        except AttributeError:
            return None

    @property
    def resolved_handler(self) -> Optional[BaseTargetHandler]:
        try:
            return getattr(self, "_resolved")[1]
        except AttributeError:
            return None


class DeferredTargetHandler(BaseTargetHandler):
    """
    Deferred targets are placeholder that should be resolved by the rule
    producing them as output.
    This is typically useful when generating file/folder whose name is not
    known in advance.

    example:

        from pathlib import Path
        from datetime import datetime
        @isg.rule(output="foo?")
        def generate_logfile(output: DeferredTarget[Path], rootdir: Path) -> None:
            # logfile is named something like `2022-04-09T19:50:52.041292.log`
            logfile = rootdir / f"{datetime.now().isoformat()}.log"
            output.resolve(logfile, discriminant="#")
    """

    COOKED_TYPE = DeferredTarget
    DISCRIMINANT = TargetDiscriminant("?")
    ON_DISK_TARGET = False

    def _load_previous_fingerprint(
        self, previous_fingerprint: bytes
    ) -> Optional[Tuple[Any, str, bytes]]:
        """
        Returns: (<cooked>, <discriminant>, <previous fingerprint>)
        """
        # Resolved target info has been stored in the fingerprint, so cunning !
        try:
            return pickle.loads(previous_fingerprint)
        except Exception:
            # Something wrong occured, we consider the previous fingerprint is
            # no longer compatible with the codebase and hence discard it
            return None

    def cook(
        self,
        id: ResolvedTargetID,
        previous_fingerprint: Optional[bytes],
        target_handlers_bundle: TargetHandlersBundle,
    ) -> DeferredTarget:
        target = DeferredTarget(id, target_handlers_bundle)
        if previous_fingerprint:
            try:
                (
                    resolved_cooked,
                    resolved_discriminant,
                    resolved_previous_fingerprint,
                ) = self._load_previous_fingerprint(previous_fingerprint)
            except ValueError:
                pass

            try:
                target.resolve(
                    resolved_cooked, resolved_discriminant, resolved_previous_fingerprint
                )
            except IsengardRunError:
                # The serialized data seems no longer compatible, just ignore them
                pass

        return target

    def clean(self, cooked: DeferredTarget) -> None:
        try:
            resolved_cooked, resolved_handler, _ = cooked._resolved
        except AttributeError:
            return None

        resolved_handler.clean(resolved_cooked)

    def compute_fingerprint(self, cooked: DeferredTarget) -> Optional[bytes]:
        try:
            resolved_cooked, resolved_handler, _ = cooked._resolved
        except AttributeError:
            return None

        resolved_fingerprint = resolved_handler.compute_fingerprint(resolved_cooked)
        return pickle.dumps((resolved_cooked, resolved_handler.DISCRIMINANT, resolved_fingerprint))

    def need_rebuild(self, cooked: DeferredTarget, previous_fingerprint: bytes) -> bool:
        try:
            resolved_cooked, resolved_handler, resolved_previous_fingerprint = cooked._resolved
        except AttributeError:
            return True

        if resolved_previous_fingerprint is None:
            return True

        return resolved_handler.need_rebuild(resolved_cooked, resolved_previous_fingerprint)

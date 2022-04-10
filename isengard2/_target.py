from typing import Optional, Any, TypeVar, Generic, Tuple, Type, Dict
from pathlib import Path
from struct import pack
from hashlib import sha256
from os import stat
from stat import S_ISDIR
import pickle
# from shutil import rmtree

from ._exceptions import IsengardDefinitionError
from ._const import ConstTypes


def resolve_target(target: str, config: Dict[str, ConstTypes]) -> str:
    try:
        return target.format(**config)
    except KeyError as exc:
        raise IsengardDefinitionError(
            f"Missing configuration `{exc.args[0]}` needed in `{target}`"
        )


T = TypeVar('T')


class BaseTargetHandler(Generic[T]):
    TARGET_TYPE: Type[T]

    def cook(self, id: str, previous_fingerprint: Optional[bytes]) -> Optional[T]:
        raise NotImplementedError

    def clean(self, target: T) -> None:
        raise NotImplementedError

    def compute_fingerprint(self, target: T) -> Optional[bytes]:
        raise NotImplementedError

    def need_rebuild(self, target: T, previous_fingerprint: bytes) -> bool:
        return self.compute_fingerprint(target) == previous_fingerprint


class FileTargetHandler(BaseTargetHandler):
    TARGET_TYPE = Path

    def __init__(self, discriminant: str = "#"):
        self.discriminant = discriminant

    def cook(self, id: str, previous_fingerprint: Optional[bytes]) -> Optional[Path]:
        if not id.endswith(self.discriminant):
            return None
        return Path(id[:-1])

    def clean(self, target: Path) -> None:
        try:
            target.unlink()
        except FileNotFoundError:
            pass

    def compute_fingerprint(self, target: Path) -> Optional[bytes]:
        fingerprint = bytearray(40)  # 8 bytes timestamp + 32 bytes sha256 hash
        try:
            fingerprint[:32] = pack("!q", stat(target).st_mtime)
            with open(target, "rb") as fd:
                fingerprint[32:] = sha256(fd.read()).digest()
            return fingerprint
        except FileNotFoundError:
            return None

    def need_rebuild(self, target: Path, previous_fingerprint: bytes) -> bool:
        try:
            if previous_fingerprint[:32] != pack("!q", stat(target).st_mtime):
                return True
            with open(target, "rb") as fd:
                if previous_fingerprint[32:] != sha256(fd.read()).digest():
                    return True
            return False
        except FileNotFoundError:
            return True


class FolderTargetHandler(BaseTargetHandler):
    TARGET_TYPE = Path

    def __init__(self, discriminant: str = "/"):
        self.discriminant = discriminant

    def cook(self, id: str, previous_fingerprint: Optional[bytes]) -> Optional[Path]:
        if not id.endswith(self.discriminant):
            return None
        return Path(id[:-1])

    def clean(self, target: Path) -> None:
        # TODO: be sure about that...
        # try:
        #     rmtree(target)
        # except FileNotFoundError:
        #     pass
        print(f"Now, should be doing `rm -rf {target}`")

    def compute_fingerprint(self, target: Path) -> Optional[bytes]:
        # TODO: recursively check the folder ?
        try:
            id_stats = stat(target)
            if not S_ISDIR(id_stats.st_mode):
                return None
            return pack("!q", id_stats.st_mtime)
        except FileNotFoundError:
            return None


class VirtualTargetHandler(BaseTargetHandler):
    """
    Virtual target doesn't exist on disk, hence they must always be build.
    """

    TARGET_TYPE = str

    def __init__(self, discriminant: str = "@"):
        self.discriminant = discriminant

    def cook(self, id: str, previous_fingerprint: Optional[bytes]) -> Optional[str]:
        if not id.endswith(self.discriminant):
            return None
        return id

    def clean(self, id: str) -> None:
        pass

    def compute_fingerprint(self, id: str) -> Optional[bytes]:
        return None

    def need_rebuild(self, target: str, previous_fingerprint: bytes) -> bool:
        return True


class DeferredTarget:
    __slot__ = ("target", "_resolved")

    def __init__(self, target: Any):
        self.target = target
        self._resolved = None

    def resolve(self, target: Any, handler: BaseTargetHandler) -> None:
        if not isinstance(target, handler.TARGET_TYPE):
            raise RuntimeError(f"Incorrect type for target, handler expects {handler.TARGET_TYPE}")
        if hasattr(self, "_resolved"):
            raise RuntimeError("Target already resolved !")
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

    def __init__(self, discriminant: str = "?"):
        self.discriminant = discriminant

    def _load_previous_fingerprint(self, previous_fingerprint: bytes) -> Optional[Tuple[Any, BaseTargetHandler, bytes]]:
        # Resolved target info has been stored in the fingerprint, so cunning !
        try:
            resolved_target, resolved_handler, resolved_previous_fingerprint = pickle.loads(previous_fingerprint)
        except Exception:
            # Something wrong occured, we consider the previous fingerprint is
            # no longer compatible with the codebase and hence discard it
            pass
        return resolved_target, resolved_handler, resolved_previous_fingerprint

    def cook(self, id: str, previous_fingerprint: Optional[bytes]) -> Optional[DeferredTarget]:
        if not id.endswith(self.discriminant):
            return None
        target = DeferredTarget(id)
        if previous_fingerprint:
            resolved = self._load_previous_fingerprint(previous_fingerprint)
            if resolved:
                resolved_target, resolved_handler, _ = resolved
                target.resolve(resolved_target, resolved_handler)
        return target

    def clean(self, target: DeferredTarget) -> None:
        if not target.resolved:
            return None
        resolved_target, resolved_handler = target.resolved
        resolved_handler.clean(resolved_target)

    def compute_fingerprint(self, target: DeferredTarget) -> Optional[bytes]:
        if not target.resolved:
            return None

        resolved_target, resolved_handler = target.resolved
        resolved_fingerprint = resolved_handler.compute_fingerprint(resolved_target)

        return pickle.dumps((resolved_target, resolved_handler, resolved_fingerprint))

    def need_rebuild(self, target: DeferredTarget, previous_fingerprint: bytes) -> bool:
        if not target.resolved:
            return True
        resolved_target, resolved_handler = target.resolved
        resolved = self._load_previous_fingerprint(previous_fingerprint)
        if not resolved:
            return True
        resolved_previous_fingerprint = resolved[2]
        return resolved_handler.need_rebuild(resolved_target, resolved_previous_fingerprint)

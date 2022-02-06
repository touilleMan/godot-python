from typing import Optional, Any, NewType, Union, Tuple
from abc import ABCMeta, abstractmethod, abstractproperty
from hashlib import sha256
from struct import pack
from pathlib import Path

from ._exceptions import IsengardDefinitionError
from ._utils import ConstTypes, serialize_const_data


# Absolute&configured (i.e. `/foo/../bar` is not valid) path, so that comparison is possible
StablePath = NewType("StablePath", Path)


class ConfiguredVirtualTarget(str):
    __slots__ = ()

    def __repr__(self):
        return f"<{type(self).__name__} {str(self)} >"


class VirtualTargetResolver:
    __slots__ = ("_configured", "_resolved")

    def __init__(self, configured: ConfiguredVirtualTarget):
        self._configured = configured
        self._resolved: Optional[ConstTypes] = None

    @property
    def last_run_resolved(self) -> ConstTypes:
        # TODO
        return None

    @property
    def configured(self) -> ConfiguredVirtualTarget:
        return self._configured

    def resolve(self, resolved: ConstTypes) -> None:
        self._resolved = resolved


ConfiguredTarget = Union[StablePath, ConfiguredVirtualTarget]


class Target(metaclass=ABCMeta):
    __slots__ = ("_label", "_workdir")

    def __init__(self, label: str, workdir: Path):
        self._label = label
        self._workdir = workdir

    def __repr__(self):
        return f"<{type(self).__name__} {self._label}>"

    def __eq__(self, other) -> bool:
        raise NotImplementedError()

    # def __eq__(self, other) -> bool:
    #     if not isinstance(other, type(self)):
    #         return NotImplemented
    #     return self._label == other._label and self._workdir == self._workdir

    def __hash__(self) -> int:
        return hash(self._label)

    @property
    @abstractproperty
    def discriminant(self) -> str:
        raise NotImplementedError

    @property
    def label(self) -> str:
        return self._label

    @property
    def workdir(self) -> Path:
        return self._workdir

    @abstractmethod
    def configure(self, **config: ConstTypes) -> ConfiguredTarget:
        raise NotImplementedError

    @abstractmethod
    def generate_fingerprint(self, configured: ConstTypes) -> Optional[bytes]:
        raise NotImplementedError

    @abstractmethod
    def clean(self, configured: ConstTypes) -> None:
        raise NotImplementedError


class FSTarget(Target):
    __slots__ = ()

    def configure(self, **config: ConstTypes) -> StablePath:
        try:
            configured = Path(self._label.format(**config))
        except KeyError as exc:
            raise IsengardDefinitionError(
                f"Missing configuration `{exc.args[0]}` needed in `{self._label}`"
            )
        if not configured.is_absolute():
            configured = self._workdir / configured
        return StablePath(configured.resolve())


class FileTarget(FSTarget):
    __slots__ = ()

    @property
    def discriminant(self) -> str:
        return "#"

    def generate_fingerprint(self, configured: ConstTypes) -> Optional[bytes]:
        assert isinstance(configured, Path)
        fingerprint = bytearray(40)  # 8 bytes timestamp + 32 bytes sha256 hash
        try:
            fingerprint[:32] = pack("!q", configured.stat().st_mtime)
            fingerprint[32:] = sha256(configured.read_bytes()).digest()
            return fingerprint
        except FileNotFoundError:
            return None

    def clean(self, configured: ConstTypes) -> None:
        assert isinstance(configured, Path)
        try:
            configured.unlink()
        except FileNotFoundError:
            pass


class FolderTarget(FSTarget):
    __slots__ = ()

    @property
    def discriminant(self) -> str:
        return "/"

    def generate_fingerprint(self, configured: ConstTypes) -> Optional[bytes]:
        assert isinstance(configured, Path)
        # TODO: recursively check the folder ?
        if configured.is_dir():
            return pack("!q", configured.stat().st_mtime)
        else:
            return None

    def clean(self, configured: ConstTypes) -> None:
        assert isinstance(configured, Path)
        # TODO: be sure about that...
        # import shutil
        # try:
        #     shutil.rmtree(configured)
        # except FileNotFoundError:
        #     pass
        print(f"Now, should be doing `rm -rf {configured}`")


class VirtualTarget(Target):
    __slots__ = ()

    @property
    def discriminant(self) -> str:
        return "@"

    def configure(self, **config: ConstTypes) -> ConfiguredVirtualTarget:
        try:
            return ConfiguredVirtualTarget(self._label.format(**config))
        except KeyError as exc:
            raise IsengardDefinitionError(
                f"Missing configuration `{exc.args[0]}` needed in `{self._label}`"
            )

    def generate_fingerprint(self, configured: ConstTypes) -> Optional[bytes]:
        if not isinstance(configured, Path):
            return serialize_const_data(configured)

        elif configured.is_file():
            fingerprint = bytearray(40)  # 8 bytes timestamp + 32 bytes sha256 hash
            try:
                fingerprint[:32] = pack("!q", configured.stat().st_mtime)
                hasher = sha256(str(configured).encode("utf8"))
                hasher.update(configured.read_bytes())
                fingerprint[32:] = hasher.digest()
                return fingerprint
            except FileNotFoundError:
                return None

        elif configured.is_dir():
            fingerprint = bytearray(40)  # 8 bytes timestamp + 32 bytes sha256 hash
            fingerprint[:32] = pack("!q", configured.stat().st_mtime)
            fingerprint[32:] = sha256(str(configured).encode("utf8")).digest()
            # TODO: recursively check the folder ?
            return fingerprint

        else:
            return None

    def clean(self, configured: Any) -> None:
        if isinstance(configured, Path):
            try:
                configured.unlink()
            except FileNotFoundError:
                # import shutil
                # try:
                #     shutil.rmtree(configured)
                # except FileNotFoundError:
                #     pass
                print(f"Now, should be doing `rm -rf {configured}`")

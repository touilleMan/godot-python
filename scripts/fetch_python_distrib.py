import argparse
from pathlib import Path
from urllib.request import urlopen
import shutil
import tarfile
from zstandard import ZstdDecompressor


PREBUILDS_BASE_URL = "https://github.com/indygreg/python-build-standalone/releases/download"
PLATFORM_TO_PREBUILDS = {
    "3.9.7": {
        "linux-x86_64": f"{PREBUILDS_BASE_URL}/20211017/cpython-3.9.7-x86_64-unknown-linux-gnu-pgo+lto-20211017T1616.tar.zst",
        "windows-x86": f"{PREBUILDS_BASE_URL}/20211017/cpython-3.9.7-i686-pc-windows-msvc-shared-pgo-20211017T1616.tar.zst",
        "windows-x86_64": f"{PREBUILDS_BASE_URL}/20211017/cpython-3.9.7-x86_64-pc-windows-msvc-shared-pgo-20211017T1616.tar.zst",
        "osx-x86_64": f"{PREBUILDS_BASE_URL}/20211017/cpython-3.9.7-x86_64-apple-darwin-pgo+lto-20211017T1616.tar.zst",
    }
}


def download(host_platform: str, cpython_version: str, output: Path) -> Path:
    try:
        per_platform = PLATFORM_TO_PREBUILDS[cpython_version]
    except KeyError:
        raise SystemExit(
            f"Unsupported CPython version `{cpython_version}`, valid values are: {', '.join(PLATFORM_TO_PREBUILDS.keys())}"
        )
    try:
        archive_url = per_platform[host_platform]
    except KeyError:
        raise SystemExit(f"No CPython prebuild for host_platform `{host_platform}`")
    archive_name = archive_url.rsplit("/", 1)[1]
    archive_path = output / archive_name
    if not archive_path.exists():
        print(f"Downloading {archive_url}...")
        tmp_archive_path = archive_path.parent / f"{archive_path.name}.tmp"
        with urlopen(archive_url) as infd:
            with open(tmp_archive_path, "bw") as outfd:
                outfd.write(infd.read())
        shutil.move(tmp_archive_path, archive_path)

    return archive_path


def extract(archive: Path, output: Path):
    distrib_path = output / "python"
    if not distrib_path.exists():
        print(f"Extracting {archive}...")
        with open(archive, "rb") as fh:
            dctx = ZstdDecompressor()
            with dctx.stream_reader(fh) as reader:
                with tarfile.open(mode="r|", fileobj=reader) as tf:
                    tf.extractall(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host-platform", required=True)
    parser.add_argument("--cpython-version", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    archive = download(
        host_platform=args.host_platform,
        cpython_version=args.cpython_version,
        output=args.output_dir,
    )
    extract(archive=archive, output=args.output_dir)

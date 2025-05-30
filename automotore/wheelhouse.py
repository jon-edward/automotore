from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys
import tempfile
import zipapp

from automotore._version import __version__


__all__ = ["WheelhouseConfig", "create_wheelhouse"]


with open(Path(__file__).parent / "_wh_main.py") as f:
    WHEELHOUSE_MAIN_SCRIPT = f.read().replace("{{__version__}}", __version__)


@dataclass
class WheelhouseConfig:
    """
    Configuration for wheelhouse creation
    """

    requirements: list[str] = None
    """ List of requirements to download to the wheelhouse. """

    requirements_path: Path = None
    """ Path to requirements.txt file to use for wheelhouse creation. """

    output_path: Path = Path("packages.pyz")
    """ Path to output wheelhouse file with created wheels and installation scripts. """

    python_version: str = None
    """ Python version to build wheels for (if not the current Python version). """

    platform: str = None
    """ Platform to build wheels for (if not the current platform). """

    abi: str = None
    """ ABI to build wheels for (if not the current ABI). """

    implementation: str = None
    """ Implementation to build wheels for (if not the current implementation). """

    show_command: bool = False
    """ Show the command used to create the wheelhouse. """

    dest_dir_root: Path = None
    """ Path to use as a root for the temporary directory passed to pip download. """


def create_wheelhouse(config: WheelhouseConfig = None) -> Path:
    """
    Creates a wheelhouse zip file containing wheels and installation scripts
    """

    if config is None:
        config = WheelhouseConfig()

    with tempfile.TemporaryDirectory(dir=config.dest_dir_root, prefix="automotore-") as tempdir:
        download_args = ()

        if config.requirements:
            download_args += tuple(config.requirements)
        
        if config.requirements_path:
            download_args += "--requirement", str(config.requirements_path)

        if config.python_version:
            download_args += "--python-version", config.python_version

        if config.platform:
            download_args += "--platform", config.platform

        if config.abi:
            download_args += "--abi", config.abi

        if config.implementation:
            download_args += "--implementation", config.implementation
        
        py_args = [
            sys.executable, "-m", "pip", "download", *download_args, 
            "--dest", tempdir, "--prefer-binary", "--no-cache-dir"
        ]

        if config.show_command:
            print(" ".join(py_args))

        subprocess.check_call(py_args)

        with open(Path(tempdir) / "__main__.py", "w") as f:
            f.write(WHEELHOUSE_MAIN_SCRIPT)

        zipapp.create_archive(tempdir, str(config.output_path))
        return config.output_path

from glob import glob
import logging
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import typing

# Templated in automotore/wheelhouse.py
__version__ = "{{__version__}}"

def iter_wheels(directory: Path) -> typing.Iterable[str]:
    for wheel in glob(str(directory / "*.whl")):
        yield wheel

def pip_cmd(directory: Path, pip_args: typing.Iterable[str]) -> typing.List[str]:
    if pip_args[0] == "install":
        return ["pip", *pip_args, "--find-links=" + str(directory), "--no-index"]
    return ["pip", *pip_args]

def install_all_packages(directory: Path):
    """
    Installs all packages contained in this wheelhouse
    """
    wheel_names = {Path(wheel).stem.split("-")[0] for wheel in iter_wheels(directory)}
    subprocess.check_call(pip_cmd(directory, ["install", *wheel_names]))

if __name__ == "__main__":
    parent_dir = Path(__file__).parent

    args = sys.argv

    if "--version" in args or "-v" in args:
        print(f"automotore v{__version__}")
        sys.exit(0)
    
    if "--help" in args or "-h" in args:
        print(f"usage: {args[0]} [-h] [-v] [pip_args ...] | {args[0]} [install | i]")
        sys.exit(0)
    
    args = args[1:]

    if not args:
        print("No arguments provided. Use --help for more info.")
        sys.exit(1)
    
    def run():
        if len(args) == 1 and (args[0] == "install" or args[0] == "i"):
            install_all_packages(Path(tempdir))
        else:
            subprocess.check_call(pip_cmd(Path(tempdir), args))
    
    try:
        with tempfile.TemporaryDirectory() as tempdir:
            shutil.unpack_archive(str(parent_dir), tempdir, "zip")
            run()
    
    except OSError as e:
        logging.warning(f"There was an error creating the temp directory: {e}")
        logging.warning("Falling back to using a temporary directory in the current directory")
        
        with tempfile.TemporaryDirectory(prefix="automotore-", dir=".") as tempdir:
            shutil.unpack_archive(str(parent_dir), tempdir, "zip")
            run()

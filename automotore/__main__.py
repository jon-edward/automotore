from argparse import ArgumentParser
from pathlib import Path

from automotore.wheelhouse import WheelhouseConfig, create_wheelhouse
from automotore._version import __version__


def main():
    parser = ArgumentParser(description=f"automotore - Self-contained Python wheelhouse generation for isolated environments. v{__version__}")
    
    parser.add_argument("-r", "--requirements-path", type=Path, nargs="?", default=None, help="Path to requirements.txt for wheelhouse creation")
    parser.add_argument("-o", "--output-path", type=Path, nargs="?", default=None, help="Path to output wheelhouse zip file")
    parser.add_argument("--python-version", type=str, nargs="?", default=None, help="Python version to use for wheelhouse creation (defaults to current version)")
    parser.add_argument("--platform", type=str, nargs="?", default=None, help="Platform to use for wheelhouse creation (defaults to current platform)")
    parser.add_argument("--abi", type=str, nargs="?", default=None, help="ABI to use for wheelhouse creation (defaults to current abi)")
    parser.add_argument("--implementation", type=str, nargs="?", default=None, help="Implementation to use for wheelhouse creation (defaults to current implementation)")
    parser.add_argument("--show-command", action="store_true", default=False, help="Print pip download command")
    args = parser.parse_args()

    kwargs = {}
    for key, value in vars(args).items():
        if value is not None:
            kwargs[key] = value
    
    config = WheelhouseConfig(**kwargs)
    create_wheelhouse(config)


if __name__ == "__main__":
    main()

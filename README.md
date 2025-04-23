# automotore

Self-contained Python wheelhouse generation for isolated environments.

## Installation

```bash
pip install automotore
```

## Usage

```bash
python -m automotore -r <requirements.txt> -o <packages.pyz>
```

See `python -m automotore --help` for more usage.

Once the wheelhouse is created, you can install specific packages with:

```bash
python <packages.pyz> install <package1> <package2> ...
```

This uses the pip command directly, so you can use regular pip arguments.

Alternatively, you can install all packages contained in the wheelhouse with:

```bash
python <packages.pyz> install
```

You can build for another platform than the current one, but note that you will need to specify Python version, platform, abi, and implementation. See [the relevant PEP](https://peps.python.org/pep-0425/) for a more detailed explanation of compatibility tags.

The easiest way to find the appropriate tags is to check the PyPI download file names for the packages you want to install.

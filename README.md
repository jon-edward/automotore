# automotore

**Automotore** is a command-line tool that generates a self-contained, portable Python wheelhouse (`.pyz` archive) containing prebuilt packages. It's designed for isolated or offline environments, and simplifies dependency management by packaging selected Python packages (and their dependencies) into a single executable archive.

## Installation

```bash
pip install automotore
```

## Usage

```bash
python -m automotore -r [requirements.txt] -o [packages.pyz]
```

or

```bash
python -m automotore [package1] [package2] ... -o [packages.pyz]
```

See `python -m automotore --help` for more usage.

Once built, the zero-dependency archive can be used to install any or all of the contained packages, even on systems without internet access.

You can install specific packages with:

```bash
python [packages.pyz] install [package1] [package2] ...
```

You can install all packages contained in the wheelhouse with:

```bash
python [packages.pyz] install
```

You can build for another platform than the current one, but note that you will need to specify Python version, platform, abi, and implementation. See [PEP 425](https://peps.python.org/pep-0425/) for a more detailed explanation of compatibility tags.

The easiest way to find the appropriate tags is to check the PyPI download file names for the packages you want to install.

## Comparison

- **Compared to pip download + local wheelhouse**: This is essentially what this project does under the hood. However, Automotore simplifies this workflow by automating the resolution and bundling process, and wrapping everything into an easy-to-use `.pyz`.

- **Compared to tools like pex, shiv, and pyoxidizer**: Those tools focus on creating self-contained executables for Python applications. In contrast, Automotore focuses on bundling Python packages for later installation.

## License

This project is released under the [MIT License](https://opensource.org/licenses/MIT).

from setuptools import setup, find_packages

from automotore._version import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="automotore",
    version=__version__,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "automotore = automotore.__main__:main"
        ]
    },
    description="Self-contained Python wheelhouse generation for isolated environments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="jon-edward",
    license="MIT",
    url="https://github.com/jon-edward/automotore",
    keywords=["python", "wheelhouse", "isolated", "environment", "pip"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
)

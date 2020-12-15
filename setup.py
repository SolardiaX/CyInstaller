import re

from setuptools import setup

with open("src/CyInstaller/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="CyInstaller",
    version=version,
    install_requires=[
        "click>=7.1.2",
        "cython>=0.29.21",
        "pyinstaller>=4.1",
        "pyyaml>=5.3.1",
    ]
)

import re

from setuptools import setup

with open("src/cyinstaller/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="CyInstaller",
    version=version,
    install_requires=[
        "python>=3.8,<3.13"
        "click>=8.1.6",
        "cython>=3.0.0",
        "pyinstaller>=5.13.0",
        "pyyaml>=6.0.1",
    ]
)

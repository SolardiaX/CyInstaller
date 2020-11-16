# -*- coding: utf-8 -*-

"""
    cyinstaller.main
    ~~~~~~~~~~~~~~~~~~~
    CLI Entry point of CyInstaller
    
    :copyright: (c) 2019 by DreamEx Works.
    :license: GPL-3.0, see LICENSE for more details.
"""

import os

import click

from . import __version__


@click.command()
def build_command():
    build()


if __name__ == "__main__":
    from .core import build
    build()

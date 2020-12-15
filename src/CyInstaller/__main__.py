# -*- coding: utf-8 -*-

"""
    CyInstaller.main
    ~~~~~~~~~~~~~~~~~~~
    CLI Entry point of CyInstaller
    
    :copyright: (c) 2019 by DreamEx Works.
    :license: GPL-3.0, see LICENSE for more details.
"""

import click
import sys


@click.command()
def build_command():
    from CyInstaller import __version__
    from CyInstaller.log import getLogger

    logger = getLogger(__name__)

    #try:
    logger.info('-------- Welecome to use CyInstaller v%s --------\n\n', __version__)

    from CyInstaller.core import build
    build()
    #except (InterruptedError, KeyboardInterrupt):
    #logger.info('CyInstaller executing inerrupted.')
    #except Exception as e:
    #logger.info('CyInstaller executing inerrupted with error - %s', e)

    # restore stdout
    print()
    sys.stdout = sys.__stdout__


if __name__ == "__main__":
    from pathlib import Path
    sys.path.append(str(Path('..').resolve()))
    build_command()

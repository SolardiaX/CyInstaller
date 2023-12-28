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
@click.option('--file', default='setup.yml', help='The setup config file, default is setup.yml')
def build_command(file: str):
    from cyinstaller import __version__
    from cyinstaller.log import getLogger

    logger = getLogger(__name__)

    #try:
    logger.info('-------- Welecome to use CyInstaller v%s --------\n\n', __version__)

    from cyinstaller.core import build
    build(file)
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

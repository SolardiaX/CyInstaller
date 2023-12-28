# -*- coding: utf-8 -*-

"""
    CyInstaller.main
    ~~~~~~~~~~~~~~~~~~~
    CLI Entry point of CyInstaller
"""

import click
import sys


@click.command()
@click.option('--file', default='setup.yml', help='The setup config file, default is setup.yml')
def build_command(file: str):
    from CyInstaller import __version__
    from CyInstaller.log import getLogger

    logger = getLogger(__name__)

    try:
        logger.info('-------- Welcome to use CyInstaller v%s --------\n\n', __version__)

        from CyInstaller.core import build
        build(file)

    except (InterruptedError, KeyboardInterrupt):
        logger.info('CyInstaller executing interrupted.')
    except Exception as e:
        logger.info('CyInstaller executing interrupted with error - %s', e)

    # restore stdout
    print()
    sys.stdout = sys.__stdout__


if __name__ == "__main__":
    from pathlib import Path
    sys.path.append(str(Path('..').resolve()))
    build_command()

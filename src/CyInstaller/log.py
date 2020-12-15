# -*- coding: utf-8 -*-

"""
    CyInstaller.log
    ~~~~~~~~~~~~~~~~~~~
    Log of CyInstaller
    
    :copyright: (c) 2019 by DreamEx Works.
    :license: GPL-3.0, see LICENSE for more details.
"""

import logging
import sys
from logging import Logger
from typing import Callable


class CyInstallerLogger(Logger):
    def loglist(self, msg: str, lists: list, itemfmt: Callable[[object], str] = None,
                level=logging.INFO) -> None:
        details = list(' - %s' % (itemfmt(item) if itemfmt is not None else item) for item in lists)
        self.log(level, '%s\n%s' % (msg, '\n'.join(details)))

    def write(self, output_stream):
        self.log(self.level, output_stream)

    def flush(self):
        pass


FORMAT = '%(asctime)s %(levelname)s: %(message)s'
DATEFMT = '%Y-%m-%d %H:%M:%S'
TRACE = logging.TRACE = logging.DEBUG - 5

logging.addLevelName(TRACE, 'TRACE')
logging.setLoggerClass(CyInstallerLogger)
logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt=DATEFMT, stream=sys.stdout)


# noinspection PyPep8Naming, PyTypeChecker
def getLogger(name: str) -> CyInstallerLogger:
    from logging import getLogger as baseGetLogger
    return baseGetLogger(name)

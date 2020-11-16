# -*- coding: utf-8 -*-

"""
    cyinstaller.log
    ~~~~~~~~~~~~~~~~~~~
    Log of CyInstaller
    
    :copyright: (c) 2019 by DreamEx Works.
    :license: GPL-3.0, see LICENSE for more details.
"""

import logging
from logging import getLogger, INFO, WARN, DEBUG, ERROR, FATAL

TRACE = logging.TRACE = DEBUG - 5
logging.addLevelName(TRACE, 'TRACE')

FORMAT = '%(relativeCreated)d %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = getLogger('CyInstaller')

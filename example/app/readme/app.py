# -*- coding: UTF-8 -*-


"""
    Readme.app
    -----------
    Readme Flask app
    :copyright: (c) 2020 by SolardiaX.
"""

import logging
import os
import sys

from . import app, db, init_logging
from .modules import *

logger = logging.getLogger(__name__)


def create_app():
    debug = app.config.get('DEBUG')
    port = app.config.get('PORT')

    try:
        # init app addon options
        app.url_map.strict_slashes = False
        app.root_path = os.path.dirname(os.path.abspath(__file__))
        # init logging
        init_logging(debug, app.config.get('LOGFILE_PATH'))
        # init database
        db.bind(**app.config['PONY'])
        db.generate_mapping(create_tables=True)
        # register bluepoints
        app.register_blueprint(main, url_prefix='/')
        app.register_blueprint(security, url_prefix='/security')
        # start the monitor
        logger.info("Server is running at port [%s].", port)
    except Exception as exp:
        logger.exception("Unable to start server - %s", exp)
        sys.exit(1)

    return app

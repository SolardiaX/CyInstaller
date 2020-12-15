# -*- coding: UTF-8 -*-

"""
Entrypoint of Readme
"""

import logging

from readme.app import create_app
from waitress import serve

logger = logging.getLogger(__name__)

try:
    app = create_app()
    serve(app, listen='*:' + str(app.config['PORT']), threads=20)
except (SystemExit, KeyboardInterrupt):
    logger.info("Server is shutdown.")

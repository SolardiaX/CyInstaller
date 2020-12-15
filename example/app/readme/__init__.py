# -*- coding: utf-8 -*-

"""
    Readme.__init__
    -----------
    Assets Init
    :copyright: (c) 202 by SolardiaX.
"""

import logging.config
import os
import sys
from pathlib import Path

import yaml
from flask import Flask
from flask_wtf import CSRFProtect
from pony.flask import Pony
from pony.orm import Database

application_path = ''

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.getcwd()

app = Flask(__name__)
csrf = CSRFProtect(app)

db = Database()
Pony(app)

app.config.from_json(os.path.join(application_path, 'config.json'))

if getattr(sys, 'frozen', False):
    pony_cfg = app.config.get('PONY')
    pony_cfg['filename'] = os.path.join(application_path, pony_cfg['filename'])
    app.config.update(**pony_cfg)
    print(app)


def init_logging(debug, logfile_path):
    # create the dir to store log files
    log_dir = os.path.join(application_path, logfile_path)
    log_cfg = os.path.join(application_path, 'logging.cfg.yml')

    if not os.path.exists(log_dir):
        Path(log_dir).mkdir(parents=True, exist_ok=True)

    # init logging
    with open(log_cfg, 'r') as conf:
        conf_dict = yaml.load(conf, Loader=yaml.SafeLoader)
        conf_dict['root']['level'] = 'DEBUG' if debug else 'INFO'
        conf_dict['handlers']['file']['filename'] = conf_dict['handlers']['file']['filename'] % {
            'logfile_dir': log_dir}
        logging.config.dictConfig(conf_dict)

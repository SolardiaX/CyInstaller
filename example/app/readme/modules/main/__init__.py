# -*- coding: utf-8 -*-

"""
    Readme.modules.main.__init__
    -----------
    Main Blueprint
    :copyright: (c) 2020 by SolardiaX.
"""

from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates')

from .routes import *

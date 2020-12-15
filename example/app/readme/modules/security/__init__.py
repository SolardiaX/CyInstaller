# -*- coding: utf-8 -*-

"""
    Reademe.modules.security.__init__
    -----------
    Security Blueprint
    :copyright: (c) 2020 by SolardiaX.
"""

from flask import Blueprint

security = Blueprint('security', __name__, template_folder='templates')

from .routes import *

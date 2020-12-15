# -*- coding: utf-8 -*-

"""
    Readme.modules.main.routes
    -----------
    Routes of Main Blueprint
    :copyright: (c) 2019 by DreamEx Works.
"""

from flask import render_template, redirect, url_for
from flask_security import login_required

from . import main


@main.route('/')
@login_required
def index():
    return render_template('main/index.html')


@main.route('/_static/<path:uri>')
def static_route(uri):
    return redirect(url_for('static', filename=uri))


@main.route('/_images/<path:uri>')
def image_route(uri):
    return redirect(url_for('static', filename='images/' + uri))


@main.route('/<string:uri>.html')
def html_route(uri):
    return render_template('main/%s.html' % uri)

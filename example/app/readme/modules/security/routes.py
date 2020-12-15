# -*- coding: utf-8 -*-

"""
    Readme.modules.security.routes
    -----------
    Routes of Security Blueprint
    :copyright: (c) 2019 by DreamEx Works.
"""

import logging

from flask import request, redirect, render_template, url_for
from flask_security import login_user
from flask_security.utils import hash_password
from pony.orm import db_session

from . import security
from .forms import *
from ..repo import user_datastore, Roles, Users


@security.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = user_datastore.find_user(name=form.username.data)
            if user is None:
                form.username.errors.append('Username not exist.')
            elif not user.verify_password(form.password.data):
                form.password.errors.append('Password not match.')
            else:
                login_user(user)
                return redirect(url_for('main.index'))

    return render_template('security/login.html', login_form=form)


@security.before_app_first_request
@db_session
def init_user_role():
    logger = logging.getLogger(__name__)

    role_admin = None
    if Roles.select().count() == 0:
        roles = {
            'admin': 'Admin',
        }

        for name, display in roles.items():
            role = user_datastore.create_role(name=name, display=display)
            logger.info('Created role [%s]', name)
            if name == 'admin':
                role_admin = role

    if Users.select().count() == 0:
        if role_admin is None:
            role_admin = user_datastore.find_role('admin')

        password = 'Welcome1'
        user_datastore.create_user(name='admin', display='Admin', password=hash_password(password), roles=[role_admin])
        logger.info('Init admin password [%s]', password)

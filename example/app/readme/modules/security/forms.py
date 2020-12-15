# -*- coding: utf-8 -*-

"""
    Readme.modules.security.forms
    -----------
    Forms of Security Blueprint
    :copyright: (c) 2019 by DreamEx Works.
"""

from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from ..forms import BaseForm, IdForm


class LoginForm(BaseForm):
    username = StringField('Username', validators=[DataRequired()], default='')
    password = PasswordField('Password', validators=[DataRequired()], default='')


class UserPasswordForm(IdForm):
    org_passwd = PasswordField('Origin Password', validators=[DataRequired()], default='')
    new_passwd = PasswordField('New Password', validators=[DataRequired()], default='')
    res_passwd = PasswordField('Repeat', validators=[DataRequired()], default='')

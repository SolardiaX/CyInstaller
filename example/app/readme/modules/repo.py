# -*- coding: utf-8 -*-

"""
    Readme.modules.repo
    -----------
    MySQL Database Models
    :copyright: (c) 2020 by SolardiaX.
"""

from datetime import datetime

from flask_security import UserMixin, RoleMixin, Security, PonyUserDatastore
from pony.orm import Required, Optional, Set, set_sql_debug

from .. import app, db

set_sql_debug(app.config.get('DEBUG', True))


class Users(db.Entity, UserMixin):
    _table_ = 'sys_users'

    name = Required(str, unique=True, max_len=50, index='idx_users_name')
    display = Required(str, max_len=50)
    password = Required(str, default='-', max_len=64)
    active = Required(bool, default=True, sql_default=True)
    last_login_at = Optional(datetime)
    current_login_at = Optional(datetime)
    last_login_ip = Optional(str, max_len=50)
    current_login_ip = Optional(str, max_len=50)
    login_count = Optional(int, sql_default=0)
    roles = Set("Roles", table='sys_users_roles')

    def verify_password(self, password):
        from flask_security.utils import verify_password
        return verify_password(password, self.password)


class Roles(db.Entity, RoleMixin):
    _table_ = 'sys_roles'

    name = Required(str, unique=True, max_len=10, index='idx_roles_name')
    display = Required(str, unique=True, max_len=50, index='idx_roles_display')
    users = Set("Users")

    def __eq__(self, other):
        return super(object).__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return super(object).__hash__()


user_datastore = PonyUserDatastore(db, Users, Roles)
security = Security(app, user_datastore, register_blueprint=False)

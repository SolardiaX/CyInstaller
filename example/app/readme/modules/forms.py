# -*- coding: utf-8 -*-

"""
    Readme.modules.forms
    -----------
    Base Forms of Readme
    :copyright: (c) 2020 by SolardiaX.
"""

from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField


def is_select_field(field):
    return field is not None and isinstance(field, SelectField)


class BaseForm(FlaskForm):
    def validate_errors(self):
        result = ''
        for fieldName, errorMessages in self.errors.items():
            field = self[fieldName].label.text
            for err in errorMessages:
                result += '<p>%s: %s</p>' % (field, err)

        return result


class IdForm(BaseForm):
    id = HiddenField('id', default='')

# -*- coding: utf-8 -*-

from wtforms import Form, StringField
from wtforms.validators import DataRequired, Length, Optional


class LoginForm(Form):
    username = StringField('Username:', validators=[DataRequired(), Length(min=1, max=30)])
    password = StringField('Password:', validators=[DataRequired(), Length(min=1, max=30)])
    email = StringField('Email:', validators=[Optional(), Length(min=0, max=50)])

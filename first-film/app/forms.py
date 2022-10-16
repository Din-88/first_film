from flask import url_for
from flask_wtf import FlaskForm
from wtforms import Form, validators
from wtforms import StringField, BooleanField, EmailField, PasswordField


class SignUpForm(Form):
    username  = StringField('Имя', [ validators.DataRequired(), 
                                     validators.Length(min=4, max=64) ])
    email     = EmailField('Email Адрес', [ validators.DataRequired(), 
                                            validators.Length(min=6, max=64) ])
    password  = PasswordField('Пароль', [
                            validators.DataRequired(), 
                            validators.Length(min=4, max=64),
                            validators.EqualTo('confirm', 
                                                message='Пароли должны совпадать')])
    confirm    = PasswordField('Повтор пороля', [ validators.DataRequired() ])
    accept_tos = BooleanField('Я принимаю Правила и Условия пользования',
                                [ validators.DataRequired() ])


class SignInForm(Form):
    username  = StringField('Имя или Email Адрес', [ validators.DataRequired(), 
                                                     validators.Length(min=4, max=64) ])
    password  = PasswordField('Пароль', [ validators.DataRequired(),
                            validators.Length(min=4, max=64) ])
    remember = BooleanField('Запомнить меня')


class SearchForm(FlaskForm):
    search_text = StringField('Поиск')
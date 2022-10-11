from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    remember = BooleanField("Remember Me", default=True)


class SignupForm(FlaskForm):
    email = StringField('Email:', validators=[Email()])
    name = StringField('Display Name:', validators=[DataRequired()])
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[Length(min=16)])
    confirm = PasswordField('Confirm Password:', validators=[EqualTo('password')])


class RankingForm(FlaskForm):
    ballot = HiddenField(validators=[DataRequired()])

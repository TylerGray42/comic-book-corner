from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    user_login = StringField("Логин", validators=[DataRequired()])
    user_password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    user_name = StringField("Имя", validators=[DataRequired()])
    user_login = StringField("Логин", validators=[DataRequired()])
    user_password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")

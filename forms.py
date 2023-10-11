from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from models import User


class LoginForm(FlaskForm):
    user_login = StringField("Логин", validators=[DataRequired()])
    user_password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    user_name = StringField("Имя", validators=[DataRequired()])
    user_login = StringField("Логин", validators=[DataRequired()])
    user_password = PasswordField("Пароль", validators=[DataRequired()])
    user_cpassword = PasswordField("Пароль", validators=[DataRequired(), EqualTo("user_password", message="Passwords must match !")])
    submit = SubmitField("Зарегистрироваться")

    def validate_uname(self, user_name):
        if User.query.filter_by(username=user_name.data).first():
            raise ValidationError("Username already taken!")

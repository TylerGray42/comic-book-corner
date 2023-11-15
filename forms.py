from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, SelectMultipleField, DecimalField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from models import User
from datetime import datetime


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


class PublisherForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired()])
    contact = StringField("Контакты", validators=[DataRequired()])
    image = FileField("Фотография", validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField("Добавить")


class AuthorForm(FlaskForm):
    fio = StringField("ФИО", validators=[DataRequired()])
    bio = StringField("Биография", validators=[DataRequired()])
    image = FileField("Фотография", validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField("Добавить")


class GenreForm(FlaskForm):
    title = StringField("Жанр", validators=[DataRequired()])
    submit = SubmitField("Добавить")


class ComicForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired()])
    description = StringField("Описание", validators=[DataRequired()])
    price = DecimalField("Стоимость", places=2, validators=[DataRequired()])
    year = DateField("Дата выхода", format='%Y-%m-%d', default=datetime.now())
    genres = SelectMultipleField("Жанры", coerce=int)
    publisher = SelectField("Издатель", coerce=int)
    author = SelectField("Автор", coerce=int)
    image = FileField("Фотография", validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField("Добавить")
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, SelectMultipleField, DecimalField, IntegerField
from wtforms.validators import InputRequired, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from datetime import datetime
from app.models import User


class LoginForm(FlaskForm):
    user_login = StringField("Логин", validators=[InputRequired()])
    user_password = PasswordField("Пароль", validators=[InputRequired()])
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    user_name = StringField("Имя", validators=[InputRequired()])
    user_login = StringField("Логин", validators=[InputRequired()])
    user_password = PasswordField("Пароль", validators=[InputRequired()])
    user_cpassword = PasswordField("Пароль", validators=[InputRequired(), EqualTo("user_password", message="Passwords must match !")])
    submit = SubmitField("Зарегистрироваться")

    def validate_uname(self, user_name):
        if User.query.filter_by(username=user_name.data).first():
            raise ValidationError("Username already taken!")
        

class GenreForm(FlaskForm):
    title = StringField("Название", validators=[InputRequired()])
    description = StringField("Описание")
    submit = SubmitField("Добавить")


class PublisherForm(FlaskForm):
    title = StringField("Название", validators=[InputRequired()])
    contact = StringField("Контакты")
    image = FileField("Фотография", validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField("Добавить")


class AuthorForm(FlaskForm):
    fio = StringField("ФИО", validators=[InputRequired()])
    bio = StringField("Биография")
    image = FileField("Фотография", validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField("Добавить")


class ComicForm(FlaskForm):
    title = StringField("Название", validators=[InputRequired()])
    description = StringField("Описание", validators=[InputRequired()])
    price = DecimalField("Стоимость", places=2, validators=[InputRequired()])
    amount = IntegerField("Количество", validators=[InputRequired()])
    year = DateField("Дата выхода", format='%Y-%m-%d', default=datetime.now())
    genres = SelectMultipleField("Жанры", coerce=int)
    publisher = SelectField("Издатель", coerce=int)
    author = SelectField("Автор", coerce=int)
    image = FileField("Фотография", validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField("Добавить")
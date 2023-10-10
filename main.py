from flask import Flask, render_template, redirect, url_for
from forms import LoginForm, RegisterForm
from database import SQLDB


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c9a1e7e34db4eea5c3948a949e4d71208b1460ed01322605'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"

database = SQLDB("database.sqlite")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    user_login = None
    form = LoginForm()
    if form.validate_on_submit():
        user_login = form.user_login.data
        # if user_login == 'admin' and form.user_password.data == '<PASSWORD>':
        #     return redirect('admin.html')
        if user_login:
            return redirect(url_for('user', user_login=user_login))
        form.user_login.data = ""
    return render_template('login.html', user_login=user_login, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    user_name = None
    user_login = None
    form = RegisterForm()
    if form.validate_on_submit():
        pass
    return render_template('register.html', user_name=user_name, user_login=user_login, form=form)


@app.route("/user/<user_login>", methods=['GET', 'POST'])
def user(user_login):
    return render_template("user.html", user_login=user_login)

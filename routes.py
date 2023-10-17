from forms import RegisterForm, LoginForm, PublisherForm, AuthorForm
from app import login_manager, create_app, db, bcrypt
from models import User, Order, Publisher, Author, Comic, Order_comic, Genre, Genre_comic
from flask import render_template, flash, url_for, redirect
from flask_bcrypt import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app = create_app()


@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template("index.html", title="Home", user=current_user)


# Login route
@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(login=form.user_login.data).first()
            if check_password_hash(user.password, form.user_password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("login.html", form=form, user=current_user)


# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user_name = form.user_name.data 
            user_login = form.user_login.data 
            user_password = form.user_password.data
            
            newuser = User(
                username=user_name,
                login=user_login,
                password = bcrypt.generate_password_hash(user_password),
            )
    
            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("login"))

        except Exception as e:
            flash(e, "danger")

    return render_template("register.html", form=form, user=current_user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/profile/<id>",  methods=("GET", "POST"))
def profile(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template("profile.html", user=current_user)


@app.route("/admin/",  methods=("GET", "POST"))
def admin():
    if not current_user.is_authenticated or current_user.admin != 1:
        return redirect(url_for('profile'))
    return render_template("admin.html", user=current_user)


@app.route("/add_author", methods=("GET", "POST"))
def add_author():
    if not current_user.is_authenticated or current_user.admin != 1:
        return redirect(url_for('profile'))
    
    form = AuthorForm()

    if form.validate_on_submit():
        try:
            fio = form.fio.data
            bio = form.bio.data
            image = form.image.data

            newauthor = Author(
                fio = fio,
                bio = bio,
                image = image.read(),
            )

            db.session.add(newauthor)
            db.session.commit()
            flash(f"Автор добавлен", "success")
            return redirect(url_for(admin.__name__))

        except Exception as e:
            flash(e, "danger")


    return render_template("add_author.html", form=form, user=current_user)


@app.route("/add_publisher", methods=("GET", "POST"))
def add_publisher():
    if not current_user.is_authenticated or current_user.admin != 1:
        return redirect(url_for('profile'))
    
    form = PublisherForm()

    if form.validate_on_submit():
        try:
            title = form.title.data
            contact = form.contact.data
            image = form.image.data

            newpublisher = Publisher(
                title = title,
                contact = contact,
                image = image.read(),
            )

            db.session.add(newpublisher)
            db.session.commit()
            flash(f"Издательство добавлено", "success")
            return redirect(url_for(admin.__name__))

        except Exception as e:
            flash(e, "danger")

    return render_template("add_publisher.html", form=form, user=current_user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", user=current_user), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html", user=current_user), 500
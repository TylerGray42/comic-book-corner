from forms import RegisterForm, LoginForm, PublisherForm, AuthorForm, GenreForm, ComicForm
from app import login_manager, create_app, db, bcrypt
from models import User, Order, Publisher, Author, Comic, Order_comic, Genre, Genre_comic
from flask import render_template, flash, url_for, redirect
from flask_bcrypt import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from PIL import Image


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
                image = None,
            )

            db.session.add(newauthor)
            db.session.commit()

            if image:
                image_name = f"{Author.query.filter_by(fio=fio).first().id}"
                image = Image.open(image)
                image.save(f"static/images/author/{image_name}.{image.format}", format=image.format)

                newauthor.image = f"{image_name}.{image.format}"
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
                image = None,
            )

            db.session.add(newpublisher)
            db.session.commit()

            if image:
                image_name = f"{Publisher.query.filter_by(title=title).first().id}"
                image = Image.open(image)
                image.save(f"static/images/publisher/{image_name}.{image.format}", format=image.format)

                newpublisher.image = f"{image_name}.{image.format}"
            db.session.commit()

            flash(f"Издательство добавлено", "success")
            return redirect(url_for(admin.__name__))

        except Exception as e:
            flash(e, "danger")

    return render_template("add_publisher.html", form=form, user=current_user)


@app.route("/add_genre", methods=["POST", "GET"])
def add_genre():
    if not current_user.is_authenticated or current_user.admin != 1:
        return redirect(url_for('profile'))
    
    form = GenreForm()

    if form.validate_on_submit():
        try:
            title = form.title.data

            newgenre = Genre(
                title = title,
            )

            db.session.add(newgenre)
            db.session.commit()
            flash(f"Жанр добавлен", "success")
            return redirect(url_for(admin.__name__))

        except Exception as e:
            flash(e, "danger")

    return render_template("add_genre.html", form=form, user=current_user)


@app.route("/add_comic", methods=["POST", "GET"])
def add_comic():
    if not current_user.is_authenticated or current_user.admin != 1:
        return redirect(url_for('profile'))
    
    form = ComicForm()

    # Сортировать жанры
    form.genres.choices = [(item.id, item.title) for item in Genre.query.all()]
    form.publisher.choices = [(item.id, item.title) for item in Publisher.query.all()]
    form.author.choices = [(item.id, item.fio) for item in Author.query.all()]

    if form.validate_on_submit():
        try:

            title = form.title.data
            description = form.description.data
            price = form.price.data
            year = form.year.data
            genres = form.genres.data
            publisher = form.publisher.data
            author = form.author.data
            image = form.image.data

            newcomic = Comic(
                title = title,
                description = description,
                price = float(price),
                year = str(year),
                image = None,
                publisher_id = publisher,
                author_id = author,
            )

            db.session.add(newcomic)
            db.session.commit()
            comic_id = Comic.query.filter_by(title=title, description=description).first().id

            if image:
                image = Image.open(image)
                image.save(f"static/images/comic/{comic_id}.{image.format}", format=image.format)

                newcomic.image = f"{comic_id}.{image.format}"

            for i in genres:
                newgenre_comic = Genre_comic(
                    comic_id = comic_id,
                    genre_id = i,
                )
                db.session.add(newgenre_comic)

            db.session.commit()

            flash(f"Комикс добавлен", "success")
            return redirect(url_for(admin.__name__))

        except Exception as e:
            flash(e, "danger")

    return render_template("add_comic.html", form=form, user=current_user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", user=current_user), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html", user=current_user), 500
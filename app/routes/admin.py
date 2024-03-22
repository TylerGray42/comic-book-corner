from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import current_user
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.forms import GenreForm, PublisherForm, AuthorForm, ComicForm
from app.models import Genre, Publisher, Author, Comic, Genre_comic
from app.extensions import db
from PIL import Image

admin_bp = Blueprint('admin', __name__)


@admin_bp.route("/admin")
def admin():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if current_user.admin != 1:
        return redirect(url_for('main.index', user=current_user))

    return render_template('admin/admin.html', user=current_user)


@admin_bp.route("/admin/add_genre", methods=['GET', 'POST'])
def add_genre():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    if current_user.admin != 1:
        return redirect(url_for('main.index', user=current_user))

    form = GenreForm()

    if request.method == 'POST' and form.validate_on_submit():

        try:
            newgenre = Genre(
                title=form.title.data,
                description=form.description.data
            )

            db.session.add(newgenre)
            db.session.commit()

            return jsonify({'id': newgenre.id, 'message': 'Жанр успешно добавлен!', 'category': 'success'})

        except IntegrityError as e:
            db.session.rollback()
            print(str(e))

        except SQLAlchemyError as e:
            db.session.rollback()
            print(str(e))

    head = list(form.data.keys())[:-2]
    body = ((("id", item.id), ("text", item.title), ("text", item.description), ("del_button", "Удалить")) for item in Genre.query.all())

    return render_template('admin/add_genre.html', user=current_user, form=form, head=head, body=body, item_type='genre')


@admin_bp.route("/admin/add_author", methods=['GET', 'POST'])
def add_author():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if current_user.admin != 1:
        return redirect(url_for('main.index', user=current_user))
    
    form = AuthorForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            newauthor = Author(
                fio=form.fio.data,
                bio=form.bio.data
            )

            db.session.add(newauthor)
            db.session.commit()

            if form.image.data:
                image = Image.open(form.image.data)
                image.save(f"app/static/images/author/{newauthor.id}.{image.format.lower()}", format=image.format.lower())

                newauthor.image = f"images/author/{newauthor.id}.{image.format.lower()}"
            else:
                newauthor.image = "images/placeholder.jpeg"

            db.session.commit()

            return jsonify({'id': newauthor.id, 'image_path': url_for('static', filename=newauthor.image), 'message': 'Автор успешно добавлен!', 'category': 'success'})

        except IntegrityError as e:
            db.session.rollback()
            print(str(e))

        except SQLAlchemyError as e:
            db.session.rollback()
            print(str(e))

    head = list(form.data.keys())[:-2]
    body = [(("id", item.id), ("text", item.fio), ("text", item.bio), ("image_button", "Фото", item.image), ("del_button", "Удалить")) for item in Author.query.all()]

    return render_template('admin/add_author.html', user=current_user, form=form, head=head, body=body, item_type='author')


@admin_bp.route("/admin/add_publisher", methods=['GET', 'POST'])
def add_publisher():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if current_user.admin != 1:
        return redirect(url_for('main.index', user=current_user))

    form = PublisherForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            newpublisher = Publisher(
                title=form.title.data,
                contact=form.contact.data
            )

            db.session.add(newpublisher)
            db.session.commit()

            if form.image.data:
                image = Image.open(form.image.data)
                image.save(f"app/static/images/publisher/{newpublisher.id}.{image.format.lower()}", format=image.format.lower())

                newpublisher.image = f"images/publisher/{newpublisher.id}.{image.format.lower()}"
            else:
                newpublisher.image = "images/placeholder.jpeg"
            db.session.commit()

            return jsonify({'id': newpublisher.id, 'image_path': url_for('static', filename=newpublisher.image), 'message': 'Издатель успешно добавлен!', 'category': 'success'})

        except IntegrityError as e:
            db.session.rollback()
            print(str(e))

        except SQLAlchemyError as e:
            db.session.rollback()
            print(str(e))

    head = list(form.data.keys())[:-2]
    body = [(("id", item.id), ("text", item.title), ("text", item.contact), ("image_button", "Фото", item.image), ("del_button", "Удалить")) for item in Publisher.query.all()]

    return render_template('admin/add_publisher.html', user=current_user, form=form, head=head, body=body, item_type='publisher')


@admin_bp.route("/admin/add_comic", methods=['GET', 'POST'])
def add_comic():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if current_user.admin != 1:
        return redirect(url_for('main.index', user=current_user))

    form = ComicForm()

    # Сортировать жанры
    form.genres.choices = [(item.id, item.title) for item in Genre.query.all()]
    form.publisher.choices = [(item.id, item.title) for item in Publisher.query.all()]
    form.author.choices = [(item.id, item.fio) for item in Author.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        try:
            newcomic = Comic(
                title=form.title.data,
                description=form.description.data,
                price=float(form.price.data),
                amount=int(form.amount.data),
                year=str(form.year.data),
                publisher_id=form.publisher.data,
                author_id=form.author.data
            )

            db.session.add(newcomic)
            db.session.commit()

            if form.image.data:
                image = Image.open(form.image.data)
                image.save(f"app/static/images/comic/{newcomic.id}.{image.format.lower()}", format=image.format.lower())

                newcomic.image = f"images/comic/{newcomic.id}.{image.format.lower()}"
            else:
                newcomic.image = "images/placeholder.jpeg"

            for i in form.genres.data:
                newgenre_comic = Genre_comic(
                    comic_id = newcomic.id,
                    genre_id = i,
                )
                db.session.add(newgenre_comic)

            db.session.commit()

            return jsonify({'id': newcomic.id, 
                            'image_path': url_for('static', filename=newcomic.image), 
                            'genres': ", ".join(i[0] for i in db.session.query(Genre.title).join(Genre_comic, Genre.id == Genre_comic.genre_id).filter(Genre_comic.comic_id == newcomic.id).all()),
                            'author': Author.query.filter_by(id=newcomic.author_id).first().fio,
                            'publisher': Publisher.query.filter_by(id=newcomic.publisher_id).first().title,
                            'message': 'Комикс успешно добавлен!', 
                            'category': 'success'})

        except IntegrityError as e:
            db.session.rollback()
            print(str(e))

        except SQLAlchemyError as e:
            db.session.rollback()
            print(str(e))

    head = list(form.data.keys())[:-2]
    body = [(("id", item.id), 
             ("text", item.title), 
             ("text", item.description), 
             ("text", item.price), 
             ("text", item.amount), 
             ("text", item.year), 
             ("text", ", ".join(i[0] for i in db.session.query(Genre.title).join(Genre_comic, Genre.id == Genre_comic.genre_id).filter(Genre_comic.comic_id == item.id).all())),  # genres
             ("text", Publisher.query.filter_by(id=item.publisher_id).first().title), 
             ("text", Author.query.filter_by(id=item.author_id).first().fio), 
             ("image_button", "Фото", item.image), 
             ("del_button", "Удалить")) for item in Comic.query.all()]

    return render_template('admin/add_comic.html', user=current_user, form=form, head=head, body=body, item_type='comic')


@admin_bp.route("/admin/delete_item", methods=['GET', 'DELETE'])
def delete_item():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if current_user.admin != 1:
        return redirect(url_for('main.index', user=current_user))

    item_id = request.args.get('id')
    item_type = request.args.get('item_type')

    match item_type:
        case 'genre':
            Genre.query.filter_by(id=item_id).delete()
            db.session.commit()
            return jsonify({'message': 'Жанр успешно удален!', 'category': 'success'})
        case 'author':
            Author.query.filter_by(id=item_id).delete()
            db.session.commit()
            return jsonify({'message': 'Автор успешно удален!', 'category': 'success'})
        case 'publisher':
            Publisher.query.filter_by(id=item_id).delete()
            db.session.commit()
            return jsonify({'message': 'Издатель успешно удален!', 'category': 'success'})
        case 'comic':
            Comic.query.filter_by(id=item_id).delete()
            db.session.commit()
            return jsonify({'message': 'Комикс успешно удален!', 'category': 'success'})
        case _:
            pass 

    return render_template('admin/add_comic.html', user=current_user)

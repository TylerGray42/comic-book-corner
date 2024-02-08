from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import current_user
from app.models import Genre, Publisher, Author, Comic
from app.extensions import db


catalog_bp = Blueprint('catalog', __name__)


# 16 комиксов на странице, 10 страниц -> подгрузка 160 комиксов. а-а-а.
@catalog_bp.route("/catalog", methods=['GET', 'POST'])
def catalog():

    # Разделитель +
    authors = request.args.get('author')
    publishers = request.args.get('publisher')
    genres = request.args.get('genre')
    page_number = request.args.get('page')
    if not page_number:
        page_number = 1


    author_list = ((item.id, item.fio) for item in Author.query.all())
    publisher_list = ((item.id, item.title) for item in Publisher.query.all())
    genre_list = ((item.id, item.title) for item in Genre.query.all())
    comic_list = ((item.id, 
                   item.title, 
                   item.description[:125] + "..." if len(item.description) > 125 else item.description,
                   item.price) for item in Comic.query.slice(8*(int(page_number)-1), 8*(int(page_number))).all())


    return render_template('catalog/catalog.html',
                           user=current_user,
                           author_list=author_list,
                           publisher_list=publisher_list,
                           genre_list=genre_list,
                           comic_list=comic_list)

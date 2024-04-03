from math import ceil
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import current_user
from sqlalchemy import union
from sqlalchemy.orm import joinedload
from app.models import Genre, Genre_comic, Publisher, Author, Comic, Order_comic, Order
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
    search_value = request.args.get('search_value')

    comic_on_page = 8

    if not page_number:
        page_number = 1

    comic_filter_1 = db.session.query(Comic).join(Genre_comic).filter(Genre_comic.genre_id.in_(list(map(int, genres.split("+")))), 
                                                                      Genre_comic.comic_id == Comic.id).subquery() if genres else db.session.query(Comic).subquery()
        
    comic_filter_2 = db.session.query(comic_filter_1).filter(comic_filter_1.c.author_id.in_(list(map(int, authors.split("+")))) if authors else True,
                                                  comic_filter_1.c.publisher_id.in_(list(map(int, publishers.split("+")))) if publishers else True).distinct().subquery()
    
    comics = db.session.query(comic_filter_2).filter(comic_filter_2.c.title.contains(search_value if search_value else ""))

    pages = ceil(len(comics.all()) / comic_on_page)

    comics = comics.slice(comic_on_page*(int(page_number)-1), comic_on_page*(int(page_number))).all()

    order = db.session.query(Order).filter(Order.user_id == current_user.id, Order.order_completed == 0).first()
    if order:
        user_order = [i.id for i in db.session.query(Comic).join(Order_comic).filter(Order_comic.order_id == order.id).options(joinedload(Comic.order_comic)).all()]

    author_list = ((item.id, item.fio) for item in Author.query.all())
    publisher_list = ((item.id, item.title) for item in Publisher.query.all())
    genre_list = ((item.id, item.title) for item in Genre.query.all())
    # 0 - comic.id, 1 - comic.title, 2 - comic.description, 3 - comic.price, 4 - in_cart
    comic_list = ((item.id, 
                   item.title, 
                   item.description[:125] + "..." if len(item.description) > 125 else item.description,
                   item.price,
                   item.id in user_order if order else False) for item in comics)


    return render_template('catalog/catalog.html',
                           user=current_user,
                           author_list=author_list,
                           publisher_list=publisher_list,
                           genre_list=genre_list,
                           comic_list=comic_list, 
                           search_value = search_value,
                           pages=pages)


@catalog_bp.route("/catalog/add_to_cart", methods=["POST"])
def add_to_cart():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    try:
        data = request.get_json()

        comic_id = data.get("comicId")
        order = db.session.query(Order).filter(Order.user_id == current_user.id, Order.order_completed == 0).first()

        if not order:
            order = Order(
                time = None,
                order_completed = False,
                user_id = current_user.id,
            )
            db.session.add(order)
            db.session.commit()

        new_order_comic = Order_comic(
            count = 1,
            order_id = order.id,
            comic_id = comic_id,
        )

        db.session.add(new_order_comic)
        db.session.commit()

        return jsonify({'category': 'success', 'message': 'Товар добавлен корзины'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}) 

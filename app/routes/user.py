from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from sqlalchemy.orm import joinedload
from app.models import Order, Order_comic, Comic, Author
from app.extensions import db

user_bp = Blueprint('user', __name__)


@user_bp.route("/profile/<id>")
def profile(id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    return render_template('user/profile.html', user=current_user)


@user_bp.route("/profile/<id>/cart")
def cart(id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
        
    order = db.session.query(Order).filter(Order.user_id == current_user.id, Order.order_completed == 0).first()
    if not order:
        order = Order(
            time = None,
            order_completed = False,
            user_id = current_user.id,
        )
        db.session.add(order)
        db.session.commit()
    comics = db.session.query(Comic).join(Order_comic).filter(Order_comic.order_id == order.id).options(joinedload(Comic.order_comic)).all()
    cart_list = ((comic,
                  db.session.query(Author).filter(Author.id == comic.author_id).first(),
                  db.session.query(Order_comic).filter(Order_comic.order_id == order.id, Order_comic.comic_id == comic.id).first()
                  ) for comic in comics)


    return render_template('user/cart.html', user=current_user, cart_list=cart_list)


@user_bp.route("/profile/<id>/cart/change_count", methods=["POST"])
def change_count(id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    

    try:
        data = request.get_json()

        order_comic_id = data.get('orderId')
        newValue = data.get('newValue')

        db.session.query(Order_comic).filter(Order_comic.id == order_comic_id).first().count = newValue
        db.session.commit()

        return jsonify({'category': 'success', 'message': 'Количество товара изменено'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}) 
    

@user_bp.route("/profile/<id>/cart/delete_order", methods=["DELETE"])
def delete_order(id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    

    try:
        data = request.get_json()

        order_comic = db.session.query(Order_comic).filter(Order_comic.id == data.get('orderId')).first()
        db.session.delete(order_comic)
        db.session.commit()

        return jsonify({'category': 'success', 'message': 'Товар удален из корзины'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}) 
    

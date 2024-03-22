from flask import Blueprint, render_template, redirect, url_for
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
    
# Отслеживать change на input 
    
    order = db.session.query(Order).filter(Order.user_id == current_user.id, Order.order_completed == 0).first()
    comics = db.session.query(Comic).join(Order_comic).filter(Order_comic.order_id == order.id).options(joinedload(Comic.order_comic)).all()
    cart_list = ((comic,
                  db.session.query(Author).filter(Author.id == comic.author_id).first(),
                  db.session.query(Order_comic).filter(Order_comic.order_id == order.id, Order_comic.comic_id == comic.id).first()
                  ) for comic in comics)

    # cart_list = comics

    return render_template('user/cart.html', user=current_user, cart_list=cart_list)

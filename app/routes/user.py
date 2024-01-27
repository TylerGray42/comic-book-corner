from flask import Blueprint
from flask import render_template, redirect, url_for
from flask_login import current_user

user_bp = Blueprint('user', __name__)

@user_bp.route("/profile/<id>")
def profile(id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    return render_template('user/profile.html', user=current_user)

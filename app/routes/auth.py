from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, logout_user, login_user, login_manager
from flask_bcrypt import check_password_hash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.forms import LoginForm, RegisterForm 
from app.models import User
from app.extensions import db, bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(login=form.user_login.data).first()
            if check_password_hash(user.password, form.user_password.data):
                login_user(user)
                return redirect(url_for('catalog.catalog'))
            else:
                flash("Ошибка логина или пароля!", "danger")
        
        except AttributeError as e:
            print(str(e))
            flash("Ошибка в логине пользователя", "danger")

        except IntegrityError as e:
            db.session.rollback() 
            print(str(e))
            flash("Ошибка при входе в аккаунт", "danger")
        
        except SQLAlchemyError as e:
            db.session.rollback() 
            print(str(e))

    return render_template('auth/login.html', user=current_user, form=form)


@auth_bp.route('/register', methods=['POST', 'GET'])
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
            return redirect(url_for("auth.login"))

        except IntegrityError as e:
            db.session.rollback() 
            print(str(e))
            flash("Ошибка при регистрации аккаунта", "danger")
        
        except SQLAlchemyError as e:
            db.session.rollback() 
            print(str(e))

    return render_template('auth/register.html', user=current_user, form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

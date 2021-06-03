from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import current_user
from flask_login.utils import login_user, logout_user

from yumroad.extensions import db, login_manager
from yumroad.models import User
from yumroad.forms import LoginForm, SignupForm

bp_user = Blueprint('user', __name__)
#user loader take in a User ID and return out
#User object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    flash('Vui lòng đăng nhập Foxv ID', 'warning')
    session['after_login'] = request.url #Flash into url => session co flash, du cho flash nam tren hay nam duoi session['after]
    print(session)
    return redirect( url_for('user.login') )

@bp_user.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()
    if form.validate_on_submit():
        #create a user
        user = User.create(form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
         #Dang nhap san
        login_user(user)
        flash('Đã đăng ký thành công', 'success')
        #we need to tell flask_login How to know that a Cookie belongs to a specific user (User cu the) 
        return redirect(url_for('products.index'))
    return render_template('/users/register.html', form=form)

@bp_user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #if current User is login
    if current_user.is_authenticated:
        flash("Tài khoản đang được đăng nhập", "warning")
        return redirect(url_for('products.index'))
    if form.validate_on_submit():
        #When login user that not create
        user = User.query.filter_by(email=form.email.data).one() #one = gap la dung tim
        login_user(user=user)
        #flash = Show messages
        flash('Đăng nhập thành công', 'success')
        #we need to tell flask_login How to know that a Cookie belongs to a specific user (User cu the)
        #Neu login xong thi quay lai vi tri url truoc hoac ve index
        return redirect(session.get('after_login') or url_for('products.index'))
    return render_template('/users/login.html', form=form)

@bp_user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('products.index'))
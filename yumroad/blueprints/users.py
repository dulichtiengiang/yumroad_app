from itertools import product
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user


from yumroad.extensions import db, login_manager
from yumroad.models import User
from yumroad.forms import LoginForm, SignupForm

bp_user = Blueprint('user', __name__)
#user loader take in a User ID and return out
#User object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

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
        #we need to tell flask_login How to know that a Cookie belongs to a specific user (User cu the) 
        return redirect(url_for('products.index'))
    return render_template('users/register.html', form=form)

@bp_user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #if current User is login
    if current_user.is_authenticated:
        flash("Ban da dang nhap roi", "Luu y")
        return redirect(url_for('products.index'))
    if form.validate_on_submit():
        #When login user that not create
        user = User.query.filter_by(email=form.email.data).one() #one = gap la dung tim
        login_user(user)
        #flash = Show messages
        flash("Login thanh cong", "Chuc mung")
        #we need to tell flask_login How to know that a Cookie belongs to a specific user (User cu the) 
        return redirect(url_for('products.index'))
    return render_template('users/login.html', form=form)

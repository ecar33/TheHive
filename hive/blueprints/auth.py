from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from hive.core.extensions import db
from hive.forms import LoginForm, SignupForm
from hive.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()
        user: User = db.session.execute(db.select(User).where(User.username == username)).scalars().first()
        if user and user.validate_password(password):
            login_user(user)
            flash(f'Successfully signed in, welcome {username}', 'success')        
            return redirect(url_for('main.index'))
        flash('User not found or password was incorrect, try again.', 'error')        
        return redirect(url_for('auth.login'))    
    return render_template('login.html', form=form)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()
        exists = db.session.execute(db.select(User).where(User.username == username)).scalars().first()
        
        if not exists:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('User successfully created! Please sign in.', 'success')        
            return redirect(url_for('auth.login'))
        else:
            flash('User already exists, please use a different username.', 'error')     
            return redirect(url_for('auth.signup'))
    return render_template('signup.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye!')
    return redirect(url_for('auth.login'))

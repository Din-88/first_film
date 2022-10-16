
import datetime
from flask import abort
from flask import redirect, render_template, request, url_for
from flask_login import LoginManager
from flask_login import confirm_login, login_user, logout_user, login_required

from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy

from . import home
from .. models import User
from .. utils import is_safe_url
from .. forms import SignUpForm, SignInForm


db = SQLAlchemy()


login_manager = LoginManager(app)
login_manager.refresh_view = 'home.signin'
login_manager.needs_refresh_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@home.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(
            username = form.username.data,
            email    = form.email.data,
            role     = 'user'
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.signin'))

    return render_template('signup.html', form=form)

@home.route('/signup_check', methods=['GET', 'POST'])
def signup_check():
    email = request.args.get('email', default = None, type = str)
    username = request.args.get('username', default = None, type = str)

    if email and User.query.filter_by(email=email).scalar():
        return 'email'
    elif username and User.query.filter_by(username=username).scalar():
        return 'username'
    
    return 'ok'


@home.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(email=username).first() or \
               User.query.filter_by(username=username).first()
        
        if user and user.check_password(password=password):
            user.last_login = datetime.datetime.utcnow()
            login_user(
                user=user,
                remember=remember, 
                duration=None,
                fresh=True
                )
            # confirm_login()
            user = db.session.merge(user)
            db.session.add(user)            
            db.session.commit()

            next = request.args.get('next')

            if not is_safe_url(target=next):
                return abort(400)
            return redirect(next or url_for('.index'))
        else:
            form.form_errors.append('Неправильное имя пользователя или пароль')

    return render_template('signin.html', form=form)

@home.route('/signout', methods=['GET', 'POST'])
@login_required
def signout():
    logout_user()
    return redirect(url_for('.index'))

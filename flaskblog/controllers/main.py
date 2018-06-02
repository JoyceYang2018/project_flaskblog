#coding:utf-8

from os import path
from uuid import uuid4

from flask import flash,url_for,redirect,render_template,Blueprint
from flask_login import login_user,logout_user
from flaskblog.forms import LoginForm,RegisterForm

from flaskblog.models import db,User
from flask_principal import Identity,AnonymousIdentity,identity_changed,current_app


main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder=path.join(path.pardir,'templates','main')
)


@main_blueprint.route('/')
def index():
    return redirect(url_for('blog.home'))


@main_blueprint.route('/login',methods=['GET','POST'])
def login():
    """登录的视图函数"""

    #先检查一下
    form = LoginForm()

    if form.validate_on_submit():

        #用session检查用户登录状态，把用户名加入cookie，
        user = User.query.filter_by(username=form.username.data).one()
        #用Flask-Login来处理登录状态
        login_user(user,remember=form.remember.data)

        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.id)
        )

        flash('You have been logged in.',category='success')
        return redirect(url_for('blog.home'))

    return render_template('login.html',form=form)


@main_blueprint.route('/logout',methods=['GET','POST'])
def logout():

    logout_user()

    identity_changed.send(
        current_app._get_current_object(),
        identity = AnonymousIdentity()
    )

    flash('You have been logged out.',category='success')
    return redirect(url_for('main.login'))


@main_blueprint.route('/register',methods=['GET','POST'])
def register():

    #先进行验证
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(id=str(uuid4()),
                        username=form.username.data,
                        password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash('Your user has been created,please login.',category='success')

        return redirect(url_for('main.login'))

    return render_template('register.html',form=form)

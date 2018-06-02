#coding:utf-8

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_principal import Principal,Permission,RoleNeed
from flask_celery import Celery
from flask_mail import Mail
from flask_cache import Cache
from flask_assets import Environment,Bundle
from flask_admin import Admin
from flask_restful import Api

#创建bcrypt实例
bcrypt = Bcrypt()

#创建Flask-Login实例
login_manager = LoginManager()

login_manager.login_view = 'main.login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Please login to access this page.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.filter_by(id=user_id).first()

#创建principal实例
principals = Principal()

#设置了三种权限，会绑定到identity之后才发挥作用
admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))

#创建celery实例
flask_celery = Celery()

#创建mail实例
mail = Mail()

#创建cache实例
cache = Cache()

#创建assets实例
assets_env = Environment()
main_css = Bundle(
    'css/bootstrap.css',
    filters='cssmin',
    output='assets/css/common.css'
)

main_js = Bundle(
    'js/bootstrap.js',
    'js/jquery-3.3.1.min.js',
    filters='jsmin',
    output='assets/js/common.js'
)

#创建admin实例
flask_admin = Admin()

#创建api实例
restful_api=Api()
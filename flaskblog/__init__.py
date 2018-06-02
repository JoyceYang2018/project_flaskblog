#coding:utf-8


from flask import Flask,redirect,url_for
from flaskblog.config import DevConfig
from flaskblog.models import db,Reminder,User,Post,Role,Tag#,BrowseVolume
from flaskblog.controllers import blog,main,admin
from flaskblog.extensions import bcrypt,login_manager,principals,flask_celery,cache
from flask_principal import identity_loaded,UserNeed,RoleNeed
from sqlalchemy import event
from flaskblog.tasks import on_reminder_save
from flask_login import current_user
from flaskblog.extensions import assets_env,main_css,main_js,cache,flask_admin,restful_api
from flaskblog.controllers.admin import CustomView,CustomModelView
from flaskblog.controllers.flask_restful.posts import PostApi
from flaskblog.controllers.flask_restful.auth import AuthApi

import os


def create_app(object_name):
    """用工厂模式创建app实例"""

    app = Flask(__name__)

    # # Get the config from the object of DevConfig
    # # 使用config.from_object()而不使用app.config['DEBUG']是因为这样可以加载class
    # app.config.from_object(DevConfig)

    app.config.from_object(object_name)

    db.init_app(app)

    #通过app对象初始化bcypt
    bcrypt.init_app(app)

    # #import the views module
    # views = __import__('views')

    login_manager.init_app(app)

    principals.init_app(app)

    flask_celery.init_app(app)

    cache.init_app(app)

    assets_env.init_app(app)
    assets_env.register('main_js',main_js)
    assets_env.register('main_css',main_css)

    flask_admin.init_app(app)
    flask_admin.add_view(CustomView(name='Custom'))
    models = [Post,Role,Tag,Reminder]#,BrowseVolume
    for model in models:
        flask_admin.add_view(
            CustomModelView(model,db.session,category='Models')
        )
    flask_admin.add_view(
        admin.CustomFileAdmin(os.path.join(os.path.dirname(__file__),'static'),
                              '/static',
                              name = 'Static Files')
    )


    restful_api.add_resource(
        PostApi,
        '/api/posts',
        '/api/posts/<string:post_id>',
        endpoint = 'restful_api_post'
    )

    restful_api.add_resource(
        AuthApi,
        '/api/auth',
        endpoint = 'restful_api_auth'
    )

    restful_api.init_app(app)







    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender,identity):
        #把Need对象加入Role
        identity.user = current_user

        #把UserNeed加入identity user对象中
        if hasattr(current_user,'id'):
            identity.provides.add(UserNeed(current_user.id))

        #把每一个role加入identity user对象中
        if hasattr(current_user,'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))




    # #指定URL='/'的路由规则
    # #当访问http://server_ip/GET(Default)时，call home()
    @app.route('/')
    def index():
        return redirect(url_for(('blog.home')))


    app.register_blueprint(blog.blog_blueprint)
    app.register_blueprint(main.main_blueprint)



    event.listen(Reminder,'after_insert',on_reminder_save)


    return app

# if __name__ == '__main__':
#     #Entry the application
#     app.run()
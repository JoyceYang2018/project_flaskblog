#coding:utf-8

import os

from celery import Celery

from flaskblog import create_app

def make_celery(app):
    #创建celery进程

    #用app配置初始化celery对象
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKEN_URL']
    )

    celery.conf.update(app.config)
    TaskBase = celery.Task


    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            #创建实例的时候被调用
            with app.app_context():
                return TaskBase.__call__(self,*args,**kwargs)

    celery.Task = ContextTask
    return celery


env = os.environ.get('BLOG_ENV','dev')
flask_app = create_app('flaskblog.config.%sConfig'%env.capitalize())
#1.每一个celery进程都要创建FLASK app
#2.把celery类注册到app中
celery = make_celery(flask_app)#让每个celery进程都包含偶app对象的上下文
#coding:utf-8

#import Flask Script object
from flask_script import Manager,Server
from flask_migrate import Migrate,MigrateCommand
from flaskblog import models,create_app

import os

env = os.environ.get('BLOG_ENV','dev')

app=create_app('flaskblog.config.%sConfig'%env.capitalize())


#Init manager object via app object
manager = Manager(app)

#init migrate object via app object
migrate = Migrate(app, models.db)

#Create a new commands:server
#This command will be run the Flask development_env server
manager.add_command("server",Server(host='127.0.0.1',port=8089))
manager.add_command('db',MigrateCommand)

@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    #确保有导入Flask app object,否则启动的CLI上下文中仍然没有app对象
    #一些flask的扩展只有在flask app object被创建之后才会被初始化，非常依赖应用上下文的环境
    #所以通过manage.py来执行命令行十分有必要
    return dict(app=app,
                db = models.db,
                User = models.User,
                Post = models.Post,
                Comment = models.Comment,
                Tag = models.Tag,
                Role = models.Role,
                Server=Server)


if __name__ == '__main__':
    manager.run()
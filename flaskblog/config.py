#coding:utf-8

class Config(object):
    """Base config class."""
    SECRET_KEY = '05c969c679e2462e76c438e36042da49'

    RECAPTCHA_PUBLIC_KEY = ''
    RECAPTCHA_PRIVATE_KEY = ''

    CACHE_TYPE = 'simple'


class ProdConfig(Config):
    """Production config class."""
    pass


class DevConfig(Config):
    """Development config class."""
    #Open the DEBUG
    DEBUG = True
    #MySQL connection
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/flaskblog'
    CELERY_RESULT_BACKEND = "amqp://guest:guest@localhost:5672//"
    CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"

    #设置CSS/JS文件在开发过程中不打包，生产环境中才打包
    ASSETS_DEBUG = True
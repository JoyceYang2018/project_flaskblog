#coding:utf-8

from flask_sqlalchemy import SQLAlchemy
from flaskblog.extensions import bcrypt,login_manager,cache
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadSignature,SignatureExpired
from flask_login import AnonymousUserMixin
from flask import current_app


# #INIT thr sqlalchemy object
# #Will be load the SQLALCHEMY_DATABASE)URI from config.py
# #SQLAlchemy 会自动的从app对象中的DevConfig中加载链接数据库的配置项
# db = SQLAlchemy(app)

db = SQLAlchemy()


users_roles = db.Table('users_roles',
                       db.Column('user_id',db.String(45),db.ForeignKey('users.id')),
                       db.Column('role_id',db.String(45),db.ForeignKey('roles.id')))



class User(db.Model):
    """Represents Protected users."""

    #Set the name for table
    __tablename__ = 'users'
    id = db.Column(db.String(45),primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    #establish contact with Post's ForeignKey:user_id
    posts = db.relationship(
        'Post',
        backref = 'users',
        lazy = 'dynamic'
    )

    roles = db.relationship(
        'Role',
        secondary = users_roles,
        backref = db.backref('users',lazy = 'dynamic')
    )

    def __init__(self,id,username,password):
        self.id = id
        self.username = username
        self.password = self.set_password(password)

        # #设置默认的role
        # default = Role.query.filter_by(name='default').first()
        # self.roles.append(default)

    def __repr__(self):
        """Define the string format for instance of User."""
        return "<Model User `{}`>".format(self.username)

    def set_password(self,password):
        """对密码进行加密"""
        return bcrypt.generate_password_hash(password)

    def check_password(self,password):
        return bcrypt.check_password_hash(self.password,password)

    def is_authenticated(self):
        if isinstance(self,AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self,AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return unicode(self.id)


    @staticmethod
    @cache.memoize(60)
    def verify_auth_token(token):
        serializer = Serializer(
            current_app.config['SECRET_KEY']
        )
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        user = User.query.filter_by(id=data['id']).first()
        return user





class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.String(45),primary_key=True)
    name = db.Column(db.String(255),unique=True)
    description = db.Column(db.String(255))

    def __init__(self,id,name):
        self.id = id
        self.name = name


    def __repr__(self):
        return "<Model Role `{}`>".format(self.name)






posts_tags = db.Table('posts_tags',
                      db.Column('post_id',db.String(45),db.ForeignKey('posts.id')),
                      db.Column('tags_id',db.String(45),db.ForeignKey('tags.id')))





class Post(db.Model):
    """Represent Protected posts"""

    __tablename__='posts'
    id = db.Column(db.String(45),primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    #set the foreign key for post
    user_id = db.Column(db.String(45),db.ForeignKey('users.id'))
    #establish contact with comment's foreignkey:post_id
    comments = db.relationship(
        'Comment',
        backref = 'posts',
        lazy = 'dynamic'
    )
    #many to many:posts<==>tags
    tags = db.relationship(
        'Tag',
        secondary = posts_tags,
        backref = db.backref('posts',lazy = 'dynamic')
    )

    def __init__(self,title,id):
        self.title = title
        self.id = id


    def __repr__(self):
        return "<Model Post `{}`>".format(self.title)




class Tag(db.Model):
    """represent protected tags"""

    __tablename__ = 'tags'
    id = db.Column(db.String(45),primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self,name,id):
        self.name = name
        self.id =id

    def __repr__(self):
        return '<Model Tag `{}`>'.format(self.name)



class Comment(db.Model):
    """represent protected comments"""

    __tablename__ = 'comments'
    id = db.Column(db.String(45),primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.String(45),db.ForeignKey('posts.id'))

    def __init__(self,name,id):
        self.name = name
        self.id = id

    def __repr__(self):
        return '<Model Comment `{}`>'.format(self.name)



class Reminder(db.Model):
    __tablename__ = 'reminders'
    id = db.Column(db.String(45),primary_key=True)
    date = db.Column(db.DateTime())
    email = db.Column(db.String(255))
    text = db.Column(db.Text())

    def __init__(self,id,text):
        self.id = id
        self.email = text

    def __repr__(self):
        return '<Model Reminder `{}`>'.format(self.text[:20])


# class BrowseVolume(db.Model):
#     pass
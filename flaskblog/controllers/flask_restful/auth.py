#coding:utf-8

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask import abort,current_app
from flask_restful import Resource

from flaskblog.controllers.flask_restful import parsers
from flaskblog.models import User


class AuthApi(Resource):

    def post(self):

        args = parsers.user_post_parser.parse_args()
        user = User.query.filter_by(username = args['username']).first()

        if user.check_password(args['password']):
            serializer = Serializer(
                current_app.config['SECRET_KEY'],
                expires_in=600
            )
            return {'token':serializer.dumps({'id':user.id})}
        else:
            abort(401)
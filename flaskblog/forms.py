#coding:utf-8

from flask_wtf import Form,RecaptchaField
from wtforms import widgets,StringField,TextField,TextAreaField,PasswordField,BooleanField,ValidationError
from wtforms.validators import DataRequired,Length,EqualTo,URL
from flaskblog.models import User
# from wtforms import ValidationError
# import re

class RegisterForm(Form):
    username = StringField('Username',[DataRequired(),Length(max=255)])
    password = PasswordField('Password',[DataRequired()])
    confirm = PasswordField('Confirm Password',[DataRequired(),EqualTo('password')])
    # recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        #验证没通过
        if not check_validate:
            return False

        #验证用户是否已经存在
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('User with that name already exists.')
            return False

        return True


class LoginForm(Form):
    username = StringField('Username',[DataRequired(),Length(max=255)])
    password = PasswordField('Password',[DataRequired()])
    remember = BooleanField('Remenber Me')

    def validate(self):
        #默认继承父类的validate()
        check_validate = super(LoginForm, self).validate()

        #验证不通过
        if not check_validate:
            return False

        #检查用户是否存在
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password.')
            return False

        #检查密码是否正确
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password.')
            return False


        return True



class PostForm(Form):
    title = StringField('Title',[DataRequired(),Length(max=255)])
    text = TextAreaField('Blog Content',[DataRequired()])


class CommentForm(Form):
    """Form validator for comment."""

    #set some field(inputbux) for enter the data.
    #patam validators:setup list of validators
    name = StringField(
        'Name',
        validators=[DataRequired(),Length(max=255)]
    )

    text = TextField(u'Comment',validators=[DataRequired()])


class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):

        # 被调用时增加一个新的雷属性ckeditors

        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()




# def custom_email(form_object,field_object):
#     if not re.match(r"[^@+@[^@]",field_object.data):
#         raise ValidationError('Field must be a valid email address.')
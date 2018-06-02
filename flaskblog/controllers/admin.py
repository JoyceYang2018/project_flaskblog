#coding:utf-8


from flask_admin import BaseView,expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flaskblog.forms import CKTextAreaField
from flask_login import login_required,current_user
from flaskblog.extensions import admin_permission

class CustomView(BaseView):

    @expose('/')
    @login_required
    @admin_permission.require(http_exception=403)
    def index(self):
        return self.render('admin/custom.html')

    @expose('/second_page')
    @login_required
    @admin_permission.require(http_exception=403)
    def second_page(self):
        return self.render('admin/second_page.html')


class CustomModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated() and admin_permission.can()



class PostView(CustomModelView):
    #用CKTEXT代替原来的Text
    form_overrides = dict(text=CKTextAreaField)

    #用搜索框,指定搜索范围
    column_searchable_list = ('text','title')

    #指定过滤器，筛选更加精确的值
    column_filters = ('publish_date',)

    #修改PostView的模板，使用CKeditor作为文本框
    create_template = 'admin/post_edit.html'
    edit_template = 'admin/post_edit.html'


class CustomFileAdmin(FileAdmin):

    def is_accessible(self):
        return current_user.is_authenticated() and admin_permission.can()

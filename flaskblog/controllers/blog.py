#coding:utf-8

from flask import render_template,Blueprint,redirect,url_for,request,abort
from sqlalchemy import func
from flask_login import login_required,current_user
from flask_principal import Permission,UserNeed
from flaskblog.extensions import cache,admin_permission,poster_permission
from flaskblog.models import db,User,Post,Tag,Comment,posts_tags

from uuid import uuid4
import datetime,os

from flaskblog.forms import CommentForm,PostForm


blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder=os.path.join(os.path.pardir,'templates','blog'),
    url_prefix='/blog'
)


@cache.cached(timeout=7200,key_prefix='sidebar_data')
def sidebar_data():
    #get posts of recent
    recent = db.session.query(Post).order_by(Post.publish_date.desc()).limit(5).all()

    #get the tags and sort by count of posts.
    top_tags = db.session.query(Tag,func.count(posts_tags.c.post_id).label('total')).join(posts_tags).group_by(Tag).order_by('total DESC').limit(5).all()
    return recent,top_tags



@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
@cache.cached(timeout=60)
def home(page=1):
    """View function for home page"""
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page,10)

    recent,top_tags = sidebar_data()

    return render_template('home.html',posts=posts,recent=recent,top_tags=top_tags)




#在确定两次不同请求的都是同一个目标URL时才会将缓存返回，否则创建一个新的缓存
def make_cache_key(*args,**kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return (path+args).encode('utf-8')






@blog_blueprint.route('/post/<string:post_id>', methods=('GET','POST'))
@cache.cached(timeout=60,key_prefix=make_cache_key)
def post(post_id):
    """View function for post page"""

    #form object:comment
    form = CommentForm()
    #当HTTP请求是POST时，提交验证通过并把用户输入返回
    if form.validate_on_submit():
        new_comment = Comment(id = str(uuid4()),name=form.name.data)
        new_comment.text = form.text.data
        new_comment.date = datetime.datetime.now()
        new_comment.post_id = post_id
        db.session.add(new_comment)
        db.session.commit()

    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('post.html', post=post,tags=tags,comments=comments,form = form, recent=recent, top_tags=top_tags)


@blog_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    """View function for tag page"""
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('tag.html', tag=tag,posts=posts, recent=recent, top_tags=top_tags)



@blog_blueprint.route('/user/<string:username>')
def user(username):
    """view function for user page"""
    user = db.session.query(User).filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('user.html', user = user,posts=posts, recent=recent, top_tags=top_tags)


@blog_blueprint.route('/new',methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()


    if not current_user:
        return redirect(url_for('main.login'))

    if form.validate_on_submit():
        new_post = Post(id=str(uuid4()),title=form.title.data)
        new_post.text = form.text.data
        new_post.publish_date = datetime.now()

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog.home'))

    return render_template('new_post.html',form=form)


@blog_blueprint.route('/edit/<string:id>',methods=['GET','POST'])
@login_required
@poster_permission.require(http_exception=403)
def edit_post(id):
    post = Post.query.get_or_404(id)

    #保证用户市登录的
    if not current_user:
        return redirect(url_for('main.login'))

    if current_user != post.users:
        return redirect(url_for('blog.post',post_id=id))

    #当user是poster或者admin，才可以编辑文章
    permission = Permission(UserNeed(post.users.id))
    if permission.can() or admin_permission.can():
        form = PostForm()

        if form.validate_on_submit():
            post.title = form.title.data
            post.text = form.text.data
            post.published_date = datetime.now()

            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.post',post_id=post.id))
        else:
            abort(403)

        form.title.data = post.title
        form.text.data = post.text
        return render_template('edit_post.html',form=form,post=post)
import datetime

from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
ckeditor = CKEditor(app)
# ckeditor.init_app(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


class PostForm(FlaskForm):
    title = StringField(label='title', validators=[DataRequired()])
    subtitle = StringField(label='subtitle', validators=[DataRequired()])
    author = StringField(label='author', validators=[DataRequired()])
    img_url = StringField(label='image URL', validators=[DataRequired(), URL()])
    body = CKEditorField(label='body', validators=[DataRequired()])
    submit = SubmitField(label='submit')


@app.route('/')
def get_all_posts():
    # done: Query the database for all the posts. Convert the data to a python list.
    posts = db.session.execute(db.select(BlogPost)).scalars().all()
    return render_template("index.html", all_posts=posts)


# done: Add a route so that you can click on individual posts.
@app.route('/<int:post_id>')
def show_post(post_id):
    # done: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


# done: add_new_post() to create a new blog post
@app.route('/new-post', methods=['GET', 'POST'])
def add_new_post():
    form = PostForm()
    if form.validate_on_submit():
        db.session.add(BlogPost(
            # id=request.form.get('id'),
            title=request.form.get('title'),
            subtitle=request.form.get('subtitle'),
            # date=request.form.get('date'),
            date=datetime.datetime.now().strftime("%B %d, %Y"),
            body=request.form.get('body'),
            author=request.form.get('author'),
            img_url=request.form.get('img_url'),
        ))
        db.session.commit()
        jsonify({"response": {"success": "added..."}})
        return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=form, post=None)


# TODO: edit_post() to change an existing blog post
@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])  # 'PUT', 'PATCH'
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    form = PostForm(
        title=post.title,
        subtitle=post.subtitle,
        body=post.body,
        author=post.author,
        img_url=post.img_url,
    )
    if 'GET' == request.method:
        return render_template("make-post.html", form=form, post=post)
    if form.validate_on_submit():
        # post.title = request.form.get('title'),
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.body = form.body.data
        post.author = form.author.data
        post.img_url = form.img_url.data
        db.session.commit()
        # return render_template('post.html', post_id=post.id)
        return redirect(url_for('show_post', post_id=post.id))


# TODO: delete_post() to remove a blog post from the database
@app.route('/delete/<int:post_id>', methods=['GET'])  # 'DELETE'
def delete_post(post_id):
    if 'GET' == request.method:
        db.session.delete(db.get_or_404(BlogPost, post_id))
        db.session.commit()
        # return jsonify({"response": {"success": "deleted..."}}), 200
        return redirect(url_for('get_all_posts'))


# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)

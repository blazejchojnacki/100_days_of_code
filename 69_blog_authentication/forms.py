from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# done: Create a LoginForm to login existing users
class LoginForm(FlaskForm):
    name = None
    email = StringField("Your email address", validators=[DataRequired()])
    password = PasswordField("Your password", validators=[DataRequired()])
    submit = SubmitField("Log in")


# done: Create a RegisterForm to register new users
class RegisterForm(LoginForm):  # FlaskForm
    name = StringField("Your username", validators=[DataRequired()])
    # email = StringField("Your email address", validators=[DataRequired()])
    # password = PasswordField("Your password", validators=[DataRequired()])
    submit = SubmitField("register")


# done: Create a CommentForm so users can leave comments below posts
class CommentForm(FlaskForm):
    body = CKEditorField("Your Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")


from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap5

'''
python -m pip install -r requirements.txt
This will install the packages from requirements.txt for this project.
'''


# from https://flask-wtf.readthedocs.io/en/1.0.x/quickstart/
class MyForm(FlaskForm):
    email = EmailField(label='email', validators=[DataRequired(), Email()])
    password = PasswordField(label='password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label='log in')


app = Flask(__name__)
# for csrf
app.secret_key = "some secret string"
bootstrap = Bootstrap5(app)


@app.route("/")
def home():
    return render_template('index.html')


# @app.route("/login.html")
# def login():
#     return render_template('login.html')


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    form = MyForm()
    if form.validate_on_submit():
        if 'admin@email.com' == form.email.data and '12345678' == form.password.data:
            return redirect('/success.html')
        else:
            return redirect('/denied.html')
    return render_template('login.html', form=form)


@app.route('/success.html')
def success():
    return render_template('success.html')


@app.route('/denied.html')
def denied():
    return render_template('denied.html')


if __name__ == '__main__':
    app.run(debug=True)

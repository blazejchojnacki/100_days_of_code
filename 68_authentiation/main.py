from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, exc
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user  # , current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
login_manager = LoginManager(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@login_manager.user_loader
def load_user(user_id):
    if user := db.session.get(User, user_id):
        return user
    else:
        return None


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'POST' == request.method:
        new_user = User(
            email=request.form.get('email'),
            password=generate_password_hash(request.form.get('password'), method='pbkdf2:sha256', salt_length=8),
            name=request.form.get('name')
        )
        try:
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError:
            flash('this email has been used already')
            return redirect(url_for('login'))
        login_user(new_user)
        # flash('Logged in successfully.')
        return render_template('secrets.html')  # , user=request.form.get('name')
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'POST' == request.method:
        user = db.session.execute(db.select(User).where(User.email == request.form.get('email'))).first()[0]
        if check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            # flash('Logged in successfully.')
            return redirect(url_for('secrets') or url_for('home'))
        else:
            flash('wrong credentials')
    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download', methods=['GET'])
def download():
    return send_from_directory(
        directory='./static/files', path='./cheat_sheet.pdf', as_attachment=False
    )


if __name__ == "__main__":
    app.run(debug=True)  # .

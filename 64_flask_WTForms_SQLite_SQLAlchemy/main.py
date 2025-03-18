from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

API_key = '3dc75c1b38f44b37c70b0f75cdb0cee9'
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZGM3NWMxYjM4ZjQ0YjM3YzcwYjBmNzVjZGIwY2VlOSIsIm5iZiI6MTc0MTE5MzQ2OC41NCwic3ViIjoiNjdjODgwZmM4MzA1NzBkMWZkYzJhZjFjIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9._Iu6kpXiwfDFSarmRofvXSNrgCxgh7Sub4y4rsL7zCY"
}
search_result = []

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db = SQLAlchemy(app=app, model_class=Base)


# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)  #
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


class RatingMovieForm(FlaskForm):
    # id = StringField(label='id', validators=[DataRequired()])
    # title = StringField(label='title', validators=[DataRequired()])
    # year = StringField(label='year', validators=[DataRequired()])
    # description = StringField(label='description', validators=[DataRequired()])
    rating = StringField(label='rating', validators=[DataRequired()])
    # ranking = StringField(label='ranking', validators=[DataRequired()])
    review = StringField(label='review', validators=[DataRequired()])
    # img_url = StringField(label='img_url', validators=[DataRequired()])
    submit = SubmitField(label='submit')


class AddMovieForm(FlaskForm):
    # id = StringField(label='id', validators=[DataRequired()])
    title = StringField(label='title', validators=[DataRequired()])
    # year = StringField(label='year', validators=[DataRequired()])
    # description = StringField(label='description', validators=[DataRequired()])
    # rating = StringField(label='rating', validators=[DataRequired()])
    # ranking = StringField(label='ranking', validators=[DataRequired()])
    # review = StringField(label='review', validators=[DataRequired()])
    # img_url = StringField(label='img_url', validators=[DataRequired()])
    submit = SubmitField(label='submit')


@app.route('/')
@app.route("/<int:movie_id>")
def home(movie_id: int = 0):
    movies_result = update_ranking()
    # movies_result = db.session.execute(db.select(Movie).order_by(Movie.ranking)).scalars().all()
    # movies = [{'id': _.id, 'title': _.title, 'year': _.year, 'description': _.description, 'rating': _.rating,
    #            'ranking': _.ranking, 'review': _.review, 'img_url': _.img_url} for _ in movies_result]
    # if movie_id is not None:
    for movie_index in range(len(movies_result)):
        if movies_result[movie_index].id == movie_id:
            movie_id = movie_index
            break
    return render_template("index.html", movies=movies_result, movie_id=movie_id)
    # return render_template("index.html", movies=movies_result, movie_id=0)


@app.route("/update/<int:movie_id>", methods=['GET', 'POST'])
@app.route("/update", methods=['GET', 'POST'])
def update(movie_id: int = None):
    form = RatingMovieForm()
    if movie_id is not None:
        movie = db.get_or_404(Movie, movie_id)
    else:
        movie = db.get_or_404(Movie, request.args.get('movie_id'))
    if form.validate_on_submit():
        # movie.title = request.form['title']
        # movie.year = request.form['year']
        # movie.description = request.form['description']
        movie.rating = request.form['rating']
        # movie.ranking = request.form['ranking']
        movie.review = request.form['review']
        # movie.img_url = request.form['img_url']
        db.session.commit()
        return redirect(url_for('home', movie_id=movie_id))
    return render_template('edit.html', movie=movie, form=form)


def update_ranking():
    movies_result = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars().all()
    for movie_index in range(-len(movies_result), 0):
        movie = db.get_or_404(Movie, movies_result[movie_index].id)
        movie.ranking = -movie_index
        db.session.commit()
    return movies_result


@app.route("/delete", methods=['GET', 'POST'])
def delete():
    movie_id = request.args.get('movie_id')
    db.session.delete(db.get_or_404(Movie, movie_id))
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=['GET', 'POST'])
def add():
    global search_result
    if 'POST' == request.method:
        movie_title = request.form['title'].replace(' ', '%20')
        url = f"https://api.themoviedb.org/3/search/movie?query={movie_title}&include_adult=false&language=en-US&page=1"
        search_result = requests.get(url, headers=headers).json()['results']
        return redirect(url_for('select'))
    return render_template('add.html', form=AddMovieForm())


@app.route("/select", methods=['GET', 'POST'])
def select():
    global search_result
    # if 'POST' == request.method:
    movies = [{
        'id': search_result.index(_), 'title': _['title'], 'date': _['release_date']
    } for _ in search_result]
    return render_template('select.html', movies=movies)


@app.route('/select/<int:movie_id>')
def apply_selection(movie_id: int):
    # movie = search_result[int(request.args.get('movie_id'))]
    movie = search_result[movie_id]
    new_movie = Movie(
        title=movie['title'],
        year=movie['release_date'].split('-')[0],
        description=movie['overview'],
        rating=movie['vote_average'],
        ranking=10,
        review='great',
        img_url=f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('update', movie_id=new_movie.id))


def add_test_entry():
    with app.app_context():
        if len(db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars().all()) == 0:
            new_movie = Movie(
                title="Phone Booth",
                year=2002,
                description="Publicist Stuart Shepard finds himself trapped in a phone booth,"
                            " pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help,"
                            " Stuart's negotiation with the caller leads to a jaw-dropping climax.",
                rating=7.3,
                ranking=10,
                review="My favourite character was the caller.",
                img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
            )
            second_movie = Movie(
                title="Avatar The Way of Water",
                year=2022,
                description="Set more than a decade after the events of the first film, learn the story of the Sully family"
                            " (Jake, Neytiri, and their kids), the trouble that follows them,"
                            " the lengths they go to keep each other safe, the battles they fight to stay alive,"
                            " and the tragedies they endure.",
                rating=7.3,
                ranking=9,
                review="I liked the water.",
                img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
            )
            db.session.add(new_movie)
            db.session.add(second_movie)
            db.session.commit()


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    add_test_entry()
    app.run(debug=True)  # .

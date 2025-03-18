from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Book(db.Model):
    id: Mapped[str] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)  # , unique=True
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    # this allows each book object to be identified by its id when printed.
    def __repr__(self):
        return f'<Book {self.id}>'


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books_database.db"
db.init_app(app)
# all_books = []


@app.route('/')
def home():
    with app.app_context():
        books_results = db.session.execute(db.select(Book).order_by(Book.id)).scalars().all()
        books = [{'id': book.id, 'title': book.title, 'author': book.author, 'rating': book.rating}
                 for book in books_results]
        # print(books)
    return render_template('index.html', books=books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    # global all_books
    if "POST" == request.method:
        # all_books.append({key: request.form[key] for key in ['title', 'author', 'rating']})
        db.session.add(Book(**request.form.to_dict()))
        # new_book_row = Book(
        #     # id=len(all_books),  # optional
        #     title=request.form['title'],
        #     author=request.form['author'],
        #     rating=request.form['rating']
        # )
        # db.session.add(new_book_row)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    book_id = request.args.get('book_id')
    book = db.get_or_404(Book, book_id)
    if "POST" == request.method:
        book.title = request.form['title']
        book.author = request.form['author']
        book.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', book=book)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    # if "POST" == request.method:
    # db.session.delete(db.session.execute(db.select(Book).where(Book.id == book_id)).scalar())
    book_id = request.args.get('book_id')
    db.session.delete(db.get_or_404(Book, book_id))
    db.session.commit()
    return redirect(url_for('home'))


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)  # .

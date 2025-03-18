from flask import Flask, render_template
import requests

app = Flask(__name__)
API_URL = 'https://api.npoint.io/2006af1a62623d53474f'


def get_posts():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()


@app.route('/post.html/<int:identifier>')
def post(identifier):
    return render_template('post.html', post=get_posts()[int(identifier)])


@app.route('/index.html')
@app.route('/')
def home():
    return render_template('index.html', posts=get_posts())


@app.route('/<page>')
def go_to(page):
    return render_template(page)


if __name__ == '__main__':
    app.run(debug=True)  # .

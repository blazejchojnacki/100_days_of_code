from flask import Flask, render_template, url_for
import requests

app = Flask(__name__)
URL = 'https://api.npoint.io/c790b4d5cab58020d391'
posts = []


@app.route('/')
def home():
    global posts
    response = requests.get(URL)
    posts = response.json()
    return render_template("index.html", posts=posts)


@app.route('/blog/<index>')
def get_blog(index):
    return render_template("post.html", post=posts[int(index)])


if __name__ == "__main__":
    app.run()  # debug=True

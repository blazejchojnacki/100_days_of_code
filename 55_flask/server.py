from flask import Flask
import random

app = Flask(__name__)
number: int


def new_number():
    global number
    number = random.randint(0, 10)


@app.route('/')
def home():
    new_number()
    return "<h1>Guess a number between 0 and 9</h1>" \
           "<img src=https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif>"


@app.route('/<int:guess>')
def guess_number(guess):
    global number
    if guess < number:
        return '<h1>it\'s too low</h1>'
    elif guess > number:
        return '<h1>it\'s too high</h1>'
    elif guess == number:
        new_number()
        return "<h1>that's right. Let's play again</h1>"


if __name__ == '__main__':
    app.run()  # debug=True

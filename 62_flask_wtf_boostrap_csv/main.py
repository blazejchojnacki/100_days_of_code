from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

'''
python -m pip install -r requirements.txt
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


def make_iterable(emoji):
    choices = ['✘']
    choices.extend([emoji*_ for _ in range(1, 6)])
    return choices


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_URL = StringField(label='Location_URL', validators=[DataRequired(), URL()])
    open_time = StringField(label='open time', validators=[DataRequired()])
    closing_time = StringField(label='closing time', validators=[DataRequired()])
    coffee_rating = SelectField(label='coffee rating', validators=[DataRequired()], choices=make_iterable(emoji='☕️'))
    wifi_rating = SelectField(label='wifi rating', validators=[DataRequired()], choices=make_iterable(emoji='💪'))
    power_outlet_rating = SelectField(label='power outlet rating', validators=[DataRequired()],
                                      choices=make_iterable(emoji='🔌'))
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['POST', 'GET'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', 'a', newline='', encoding='utf-8') as csv_pointer:
            csv_writer = csv.writer(csv_pointer, delimiter=',')
            csv_writer.writerow([_.data for _ in form][:7])
        print([_.data for _ in form])
        return redirect('/cafes')
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
    # cafes()

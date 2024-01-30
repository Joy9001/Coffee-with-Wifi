from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL, Regexp
import pandas
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap5(app)

coffee_dict = {
    1: '☕',
    2: '☕☕',
    3: '☕☕☕',
    4: '☕☕☕☕',
    5: '☕☕☕☕☕'
}

wifi_dict = {
    0: '🙅',
    1: '💪',
    2: '💪💪',
    3: '💪💪💪',
    4: '💪💪💪💪',
    5: '💪💪💪💪💪'
}

power_dict = {
    0: '🙅',
    1: '🔌',
    2: '🔌🔌',
    3: '🔌🔌🔌',
    4: '🔌🔌🔌🔌',
    5: '🔌🔌🔌🔌🔌'
}


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps (URL)', validators=[URL()])
    open_time = StringField('Opening Time e.g. 8AM', validators=[Regexp(regex='^[1-9]|1[0-2][APap][Mm]$')])
    close_time = StringField('Closing Time e.g. 9PM', validators=[Regexp(regex='^[1-9]|1[0-2][APap][Mm]$')])
    coffee_rating = SelectField('Coffee Rating', choices=[(1, '☕'), (2, '☕☕'), (3, '☕☕☕'), (4, '☕☕☕☕'), (5, '☕☕☕☕☕')], coerce=int, validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Strength Rating', choices=[(0, '🙅'), (1, '🛜'), (2, '🛜🛜'), (3, '🛜🛜🛜'), (4, '🛜🛜🛜🛜'), (5, '🛜🛜🛜🛜🛜')], coerce=int, validators=[DataRequired()])
    socket_availability = SelectField('Power Socket Availability', choices=[(0, '🙅'), (1, '🔌'), (2, '🔌🔌'), (3, '🔌🔌🔌'), (4, '🔌🔌🔌🔌'), (5, '🔌🔌🔌🔌🔌')], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        cafe_info = {
            "Cafe Name": [form.cafe.data],
            "Location": [form.location.data],
            "Open": [form.open_time.data],
            "Close": [form.close_time.data],
            "Coffee": [coffee_dict.get(form.coffee_rating.data)],
            "Wifi": [wifi_dict.get(form.wifi_rating.data)],
            "Power": [power_dict.get(form.socket_availability.data)]
        }
        # print(cafe_info)
        data = pandas.DataFrame(cafe_info)
        data.to_csv("cafe-data.csv", mode='a', header=False, index=False)
        form.process()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    cafe_dict = pandas.read_csv("cafe-data.csv").to_dict()
    # print(cafe_dict)
    return render_template('allcafes.html', cafe_list=cafe_dict)


if __name__ == '__main__':
    app.run(debug=True)

import os
from flask import Flask, request,render_template,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, RadioField,
                    IntegerField, SelectField, SubmitField)
from wtforms.validators import DataRequired
import requests

###################################################
################ CONFIGURATIONS ###################
##################################################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


url = "https://calorieninjas.p.rapidapi.com/v1/nutrition"
headers = {
	"X-RapidAPI-Key": "API-KEY",
	"X-RapidAPI-Host": "calorieninjas.p.rapidapi.com"
}




###################################################
################ form ###########################
##################################################

class InfoForm(FlaskForm):

    main_dish = StringField(("What dish, drink, or ingredient would you like to find the nutritional value of? "), validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        session['main_dish'] = form.main_dish.data
        return redirect(url_for('nutrition_info'))
    return render_template('index.html', form=form)

@app.route('/nutrition_info', methods=['GET', 'POST'])
def nutrition_info():
    querystring = {"query":session['main_dish']}
    output = requests.request("GET", url, headers=headers, params=querystring).json()
    return render_template('nutrition_info.html', info=output)

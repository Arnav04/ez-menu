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


url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch"
headers = {
	'X-RapidAPI-Key': 'API KEY',
    'X-RapidAPI-Host': 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com'
}


###################################################
################ form ###########################
##################################################

class InfoForm(FlaskForm):

    cuisine = RadioField(u"What cuisines do you like?",
                                choices=['african', 'chinese', 'japanese',
                                'korean', 'vietnamese', 'thai', 'indian',
                                'british', 'irish', 'french', 'italian',
                                'mexican', 'spanish', 'middle eastern',
                                'jewish', 'american', 'cajun', 'southern',
                                'greek', 'german', 'nordic', 'eastern european',
                                 'caribbean', 'latin american'],
                                 validators=[DataRequired()])
    ingredients = StringField("What ingredients would you like to use?")
    meal = SelectField("What kind of meal would you like?", choices=['main course',
    'side dish', 'dessert', 'appetizer', 'salad', 'bread', 'breakfast', 'soup',
    'beverage', 'sauce', 'drink'], validators=[DataRequired()])
    search = StringField("Please enter one of your favorite dishes:",
                        validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        session['cuisine'] = form.cuisine.data
        session['ingredients'] = form.ingredients.data
        session['meal'] = form.meal.data
        session['search'] = form.search.data
        return redirect(url_for('foods'))

    return render_template('index.html', form=form)

@app.route('/foods')
def foods():
    querystring = {"query":session['search'],"cuisine":session['cuisine'],
        "diet":session['diet'],
        "includeIngredients":session['ingredients'],"type":session['meal'],
        "instructionsRequired":True,"addRecipeInformation":True}
    output = requests.request("GET", url, headers=headers, params=querystring).json()
    return render_template('foods.html', recipes=output)

if __name__ == '__main__':
    app.run(debug=True)

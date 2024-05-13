from flask import Flask, render_template, request, url_for, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, validators
import os
from pymongo import MongoClient
import certifi
from wtforms.validators import DataRequired

import main_functions

app = Flask(__name__)

credentials = main_functions.read_from_file("credentials.json")

username = credentials['username']
password = credentials['password']

app.secret_key=os.urandom(16).hex()
app.config["MONGO_URI"]="mongodb+srv://{0}:{1}@learningmongodb.ifhle6b.mongodb.net/" \
                        "?retryWrites=true&w=majority&appName=learningMongoDB".format(username, password)

mongo = PyMongo(app)

client = MongoClient("mongodb+srv://{0}:{1}@learningmongodb.ifhle6b.mongodb.net/" \
                        "?retryWrites=true&w=majority&appName=learningMongoDB".format(username, password),
                     tlsCAFile=certifi.where())

db = client['db']

years = [1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993,
         1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005,
         2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017,
         2018, 2019, 2020, 2021, 2022, 2023, 2024]

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']

days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
        31]

class UserCredentials(FlaskForm):
    app_username = StringField("app_username", [validators.DataRequired()])
    app_password = PasswordField("app_password", [validators.DataRequired()])

class Search(FlaskForm):
    year = SelectField("year",
                       choices=years)
    month = SelectField("month",
                        choices=months)
    day = SelectField("day", choices=days)


def real_username_and_password(appUsername, appPassword):
    user_credentials = db.usernameAndPassword.find()
    if user_credentials is not None:
        for i in user_credentials:
            if i['username'] == appUsername and check_password_hash(i['password'], appPassword):
                return True
        # If no matching user found
        return False
    else:
        return False

def who_was_president(month, day, year):
    president = ""
    if 1982 <= year <= 1988:
        president = 'RonaldReagan'
    elif year == 1989:
        if month == 'January' and day < 20:
            president = 'RonaldReagan'
        else:
            president = 'GeorgeHWBush'
    elif 1990 <= year <= 1992:
        president = 'GeorgeHWBush'
    elif year == 1993:
        if month == 'January' and day < 20:
            president = 'GeorgeHWBush'
        else:
            president = 'BillClinton'
    elif 1994 <= year <= 2000:
        president = 'BillClinton'
    elif year == 2001:
        if month == 'January' and day < 20:
            president = 'BillClinton'
        else:
            president = 'GeorgeWBush'
    elif 2002 <= year <= 2008:
        president = 'GeorgeWBush'
    elif year == 2009:
        if month == 'January' and day < 20:
            president = 'GeorgeWBush'
        else:
            president = 'BarackObama'
    elif 2010 <= year <= 2016:
        president = 'BarackObama'
    elif year == 2017:
        if month == 'January' and day < 20:
            president = 'BarackObama'
        else:
            president = 'DonaldTrump'
    elif 2018 <= year <= 2020:
        president = 'DonaldTrump'
    elif year == 2021:
        if month == 'January' and day < 20:
            president = 'DonaldTrump'
        else:
            president = 'JoeBiden'
    elif 2022 <= year <= 2024:
        president = 'JoeBiden'
    return president

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Search(request.form)
    if request.method == 'POST' and form.validate():
        yearSelected = int(request.form['year'])
        monthSelected = request.form['month']
        daySelected = int(request.form['day'])
        president_during_birth = who_was_president(monthSelected, daySelected, yearSelected)
        session['url'] = url_for('president_page', president=president_during_birth)
        session['url2'] = url_for('president_page', president=president_during_birth)
        return redirect(url_for('president_page', president=president_during_birth))
    return render_template("index.html", form=form)

@app.route('/<president>')
def president_page(president):
    return render_template(president + ".html")

@app.route('/logIn', methods=['GET', 'POST'])
def logIn():
    form = UserCredentials(request.form)
    if request.method == 'POST' and form.validate():
        appUsername = request.form['app_username']
        appPassword = request.form['app_password']
        # Get the presidential page URL from the session
        next_url = session.pop('url', None)
        if real_username_and_password(appUsername, appPassword):
            session['username'] = appUsername
            if next_url is not None:
                return redirect(next_url)
            else:
                return redirect(url_for('index'))
        else:
            flash('Error: Username and/or password not found', 'error')
            return render_template("logIn.html", form=form)
    return render_template("logIn.html", form=form)

@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    form = UserCredentials(request.form)
    if request.method == 'POST' and form.validate():
        newUsername = request.form['app_username']
        newPassword = request.form['app_password']
        if not real_username_and_password(newUsername, newPassword):
            db.usernameAndPassword.insert_one({'username': newUsername, 'password': generate_password_hash(newPassword, method='scrypt')})
            return render_template("accountCreated.html")
        else:
            flash('Account already exists.', 'error')
            return render_template("createAccount.html", form=form)
    return render_template("createAccount.html", form=form)

@app.route('/books')
def books():
    return render_template("books.html")

@app.route('/logOut', methods=['GET', 'POST'])
def logOut():
    if request.method == 'POST':
        next_url = session.pop('url2', None)
        if request.form.get('logout'):
            return redirect(url_for('loggedOut'))
        elif request.form.get('cancel'):
            if next_url is not None:
                return redirect(next_url)
            else:
                return redirect(url_for('index'))
    return render_template("logOut.html")

@app.route('/loggedOut')
def loggedOut():
    session.clear()
    return render_template("loggedOut.html")

app.run()




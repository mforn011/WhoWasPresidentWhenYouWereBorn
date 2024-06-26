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

# Initialize Flask app
app = Flask(__name__)

# Load credentials from credentials.json
credentials = main_functions.read_from_file("credentials.json")

username = credentials['username']
password = credentials['password']

# Configure secret key and MongoDB URI
app.secret_key="new_secret_key"
app.config["MONGO_URI"]="mongodb+srv://{0}:{1}@learningmongodb.ifhle6b.mongodb.net/" \
                        "?retryWrites=true&w=majority&appName=learningMongoDB".format(username, password)

# Initialize PyMongo
mongo = PyMongo(app)

# Connect to MongoDB client
client = MongoClient("mongodb+srv://{0}:{1}@learningmongodb.ifhle6b.mongodb.net/" \
                        "?retryWrites=true&w=majority&appName=learningMongoDB".format(username, password),
                     tlsCAFile=certifi.where())

# Access the database
db = client['db']

# Define lists for form choices
years = [1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993,
         1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005,
         2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017,
         2018, 2019, 2020, 2021, 2022, 2023, 2024]

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']

days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
        31]

# Define form for user credentials
class UserCredentials(FlaskForm):
    app_username = StringField("app_username", [validators.DataRequired()])
    app_password = PasswordField("app_password", [validators.DataRequired()])

# Define form for search
class Search(FlaskForm):
    year = SelectField("year",
                       choices=years)
    month = SelectField("month",
                        choices=months)
    day = SelectField("day", choices=days)

# Define form for new password
class NewPassword(FlaskForm):
    new_user_password = PasswordField("new_user_password", [validators.DataRequired()])
    new_user_password2 = PasswordField("new_user_password2", [validators.DataRequired()])

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
    session['url'] = request.url
    form = Search(request.form)
    if request.method == 'POST' and form.validate():
        yearSelected = int(request.form['year'])
        monthSelected = request.form['month']
        daySelected = int(request.form['day'])
        president_during_birth = who_was_president(monthSelected, daySelected, yearSelected)
        session['url'] = url_for('president_page', president=president_during_birth)
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
        next_url = ''
        if 'url' in session:
            next_url = session['url']
        if real_username_and_password(appUsername, appPassword):
            session['username'] = appUsername
            if next_url:
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
            flash('Account successfully created!', 'success')
        else:
            flash('Account already exists.', 'error')
    return render_template("createAccount.html", form=form)

@app.route('/books', methods=['GET', 'POST'])
def books():
    session['url'] = request.url
    saved_books = []
    if 'username' in session:
        user_account = db.usernameAndPassword.find_one({'username': session['username']})
        if user_account and 'book_info' in user_account:
            saved_books = user_account['book_info']
    if request.method == 'POST':
        if 'username' in session:
            book_title = request.form['book_title']
            book_image = request.form['book_image']
            book_description = request.form['book_description']
            book_url = request.form['book_url']
            book_info = {'book_title': book_title,
                         'book_image': book_image,
                         'book_description': book_description,
                         'book_url': book_url}
            if not any(book['book_title'] == book_title for book in saved_books):
                db.usernameAndPassword.update_one({"username": session['username']}, {"$push": {'book_info': book_info}})
                saved_books.append(book_info)
                return render_template("books.html", saved_books=saved_books)
        else:
            return redirect(url_for('logIn'))
    return render_template("books.html", saved_books=saved_books)

@app.route('/user', methods=['GET', 'POST'])
def user():
    session['url'] = request.url
    book_info = []
    if 'username' in session:
        user_account = db.usernameAndPassword.find_one({"username": session['username']})
        if user_account and 'book_info' in user_account:
            book_info = user_account['book_info']
    book_info_without_quotes = []
    for i in book_info:
        book_title = i['book_title'].strip('"')
        book_image = i['book_image'].strip('"')
        book_description = i['book_description'].strip('"')
        book_url = i['book_url'].strip('"')
        updated_book_info = (book_title, book_image, book_description, book_url)
        book_info_without_quotes.append(updated_book_info)
    if request.method == 'POST':
        if 'username' in session:
            bookTitle = request.form['book_title']
            bookImage = request.form['book_image']
            bookDescription = request.form['book_description']
            bookUrl = request.form['book_url']
            delete_book_info = {
                "book_title": bookTitle,
                "book_image": bookImage,
                "book_description": bookDescription,
                "book_url": bookUrl
            }
            db.usernameAndPassword.update_one({"username": session['username']}, {"$pull": {'book_info': delete_book_info}})
            return redirect(url_for('user'))
    return render_template("user.html", book_info=book_info_without_quotes)

@app.route('/user2')
def user2():
    session['url'] = request.url
    return render_template("user2.html")

@app.route('/newPassword', methods=['GET', 'POST'])
def newPassword():
    session['url'] = request.url
    form = NewPassword(request.form)
    user_name = ''
    user_password = ''
    if 'username' in session:
        user_account = db.usernameAndPassword.find_one({'username': session['username']})
        if user_account and 'password' in user_account:
            user_name = user_account['username']
            user_password = user_account['password']
    if request.method == 'POST' and form.validate:
        newPassword1 = request.form['new_user_password']
        newPassword2 = request.form['new_user_password2']
        if newPassword1 == newPassword2:
            if not check_password_hash(user_password, newPassword1):
                flash('New password saved!', 'success')
                db.usernameAndPassword.update_one({'username': user_name}, {'$set': {'password': generate_password_hash(newPassword1, method='scrypt')}})
                return render_template("newPassword.html", form=form)
            else:
                flash('That is already your password.', 'error')
                return render_template("newPassword.html", form=form)
        else:
            flash('Passwords must be typed exactly the same twice.', 'error')
            return render_template("newPassword.html", form=form)
    return render_template("newPassword.html", form=form)

@app.route('/logOut', methods=['GET', 'POST'])
def logOut():
    if request.method == 'POST':
        if 'url' in session:
            next_url = session['url']
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

if __name__ == '__main__':
    app.run()




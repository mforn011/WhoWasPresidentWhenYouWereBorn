from flask import Flask, render_template, request, url_for, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from flask_mail import Mail, Message
from wtforms import StringField, PasswordField, SelectField, validators
import os
from pymongo import MongoClient
import certifi
from wtforms.validators import DataRequired

# Initialize Flask app
app = Flask(__name__)

# Retrieve environment variables from Heroku Config Vars
mongo_username = os.getenv('MONGO_USERNAME')
mongo_password = os.getenv('MONGO_PASSWORD')

# Configure secret key and MongoDB URI
secret_key = os.getenv('SECRET_KEY')

app.secret_key = secret_key

mongo_uri=f"mongodb+srv://{mongo_username}:{mongo_password}@learningmongodb.ifhle6b.mongodb.net/" \
                        "?retryWrites=true&w=majority&appName=learningMongoDB"

app.config["MONGO_URI"]=mongo_uri

# Initialize PyMongo
mongo = PyMongo(app)

# Connect to MongoDB client
client = MongoClient(mongo_uri, tlsCAFile=certifi.where())

# Access the database
db = client['db']

# Define lists for form choices
years = list(range(1982, 2025))

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']

days = list(range(1, 32))

# Initialize Flask-Mail
my_email = os.getenv('MAIL_USERNAME')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = my_email
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)

# Define form for user credentials
class UserCredentials(FlaskForm):
    app_username = StringField("app_username", [validators.DataRequired()])
    app_password = PasswordField("app_password", [validators.DataRequired()])
    app_email = StringField("app_email", [validators.DataRequired()])

# Define form for search
class Search(FlaskForm):
    year = SelectField("year",
                       choices=years)
    month = SelectField("month",
                        choices=months)
    day = SelectField("day", choices=days)

# Define form for log-in credentials
class UserInfo(FlaskForm):
    app_username = StringField("app_username", [validators.DataRequired()])
    app_password = PasswordField("app_password", [validators.DataRequired()])

# Define form for new password
class NewPassword(FlaskForm):
    new_user_password = PasswordField("new_user_password", [validators.DataRequired()])
    new_user_password2 = PasswordField("new_user_password2", [validators.DataRequired()])

class NewEmail(FlaskForm):
    new_user_email = StringField("new_user_email", [validators.DataRequired()])

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

def real_username_and_email(appUsername, appEmail):
    user_info = db.usernameAndPassword.find()
    if user_info is not None:
        for i in user_info:
            if i['username'] == appUsername and i['email'] == appEmail:
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
    form = UserInfo(request.form)
    if request.method == 'POST' and form.validate():
        appUsername = request.form['app_username']
        appPassword = request.form['app_password']
        # Get the presidential page URL from the session
        next_url = ''
        if 'url' in session:
            next_url = session['url']
        if real_username_and_password(appUsername, appPassword):
            session['username'] = appUsername
            user_info = db.usernameAndPassword.find_one({'username': appUsername})
            if user_info and 'email' in user_info:
                session['email'] = user_info['email']
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
        newEmail = request.form['app_email']
        if not real_username_and_password(newUsername, newPassword):
            db.usernameAndPassword.insert_one({'username': newUsername, 'password': generate_password_hash(newPassword, method='scrypt'),
                                               'email': newEmail})
            session['username'] = newUsername
            session['email'] = newEmail
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
    return render_template("user2.html")

@app.route('/newPassword', methods=['GET', 'POST'])
def newPassword():
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

@app.route('/newEmail', methods=['GET', 'POST'])
def newEmail():
    form = NewEmail(request.form)
    session_username = ''
    if 'username' in session:
        session_username = session['username']
    if request.method == 'POST' and form.validate:
        new_user_email = request.form['new_user_email']
        if not real_username_and_email(session_username, new_user_email):
            session['email'] = new_user_email
            flash('New email saved!', 'success')
            db.usernameAndPassword.update_one({'username': session_username}, {'$set': {'email': new_user_email}})
            return render_template("newEmail.html", form=form)
        elif real_username_and_email(session_username, new_user_email):
            flash('That is already your email.', 'error')
            return render_template("newEmail.html", form=form)
    return render_template("newEmail.html", form=form)

@app.route('/resetPassword', methods=['GET', 'POST'])
def resetPassword():
    form = UserCredentials(request.form)
    if request.method == 'POST' and form.validate:
        user_name = request.form['app_username']
        user_email = request.form['app_email']
        if real_username_and_email(user_name, user_email):
            new_temporary_password = os.urandom(10).hex()
            db.usernameAndPassword.update_one({'username': user_name}, {
                '$set': {'password': generate_password_hash(new_temporary_password, method='scrypt')}})
            msg = Message(
                subject="New temporary password",
                sender=f"Who Was President When You Were Born?<{my_email}>",
                recipients=[user_email],
            )
            msg.body = f"Here's your new temporary password:\n{new_temporary_password}"
            mail.send(msg)
            return redirect(url_for('temporaryPasswordSent'))
        else:
            flash('Could not find any account with this username or email.', 'error')
            return render_template("resetPassword.html", form=form)
    return render_template("resetPassword.html", form=form)

@app.route('/temporaryPasswordSent')
def temporaryPasswordSent():
    return render_template("temporaryPasswordSent.html")

@app.route('/logOut')
def logOut():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()




from flask import Flask, render_template, url_for, redirect, flash, request, session, send_file, jsonify
from wtforms import Form, BooleanField, validators, PasswordField, TextField
from dbconnect import connection
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from functools import wraps
from content_management import Content
from tts import GoogleTextToSpeech
from urllib.parse import urlparse
from wikipedia import WikipediaParser
from markupsafe import escape
from querydb import queryDb
import os
import gc
app = Flask(__name__)
# app.secret_key=os.environ.get("FLASK_APP_SECRET_KEY")
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def homepage():
    try:
        if 'logged_in' in session:
            return redirect(url_for('dashboard'))
        else:
            return render_template("main.html")
    except Exception as e:
        return str(e)


@app.route('/dashboard/')
@login_required
def dashboard():

    return render_template("dashboard.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = ''
    try:
        c, conn = connection()
        if 'logged_in' in session:
            return redirect(url_for('dashboard'))
        elif request.method == "POST":
            # data = c.execute("SELECT * FROM users WHERE username = (%s)",
            #                  (thwart(request.form["username"]),))
            db = queryDb(request.form["username"], c)
            data = db.getUserData()

            data = c.fetchone()[2]

            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['userame'] = request.form['username']

                flash("You are now logged in")
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid credentials, try again."

        gc.collect()
        return render_template("login.html", error=error)

    except Exception as e:
        # flash(e)
        error = "Invalid credentials, try again."
        return render_template("login.html", error=error)


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField(
        'I accept the Terms of Service and Privacy Notice ', [validators.Required()])


@app.route('/register/', methods=["GET", "POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)
        if 'logged_in' in session:
            return redirect(url_for('dashboard'))
        elif request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()
            db = queryDb(request.form["username"], c)
            # x = c.execute("SELECT * FROM users WHERE username = (%s)",
            #               (thwart(username),))
            x = db.getUserData()
            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                # c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                #           (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))
                db.createNewUser(password, email)
                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))


@app.route('/converttospeech/<string:contentTitle>/', methods=['GET', 'POST'])
@login_required
def convertToSpeech():
    return jsonify({'txt': 'Congrats !'})


# @app.route('/converttospeech/<string:contentTitle>/', methods=['GET', 'POST'])
# @login_required
# def convertToSpeech():
#     try:
#         c, conn = connection()
#         contentTitle = escape(contentTitle)
#         url = request.form['wikiLink']
#         parsedUrl = urlparse(url)
#         # If its url to some other website
#         if parsedUrl.netloc != 'en.wikipedia.org' or parsedUrl.scheme not in ['http', 'https']:
#             return "website should be en.wikipedia.org"
#         elif parsedUrl.path == 'wiki/Main_Page':
#             return "Search for some other path"
#         else:
            
#             wikipediaLink = parsedUrl.scheme + parsedUrl.netloc + parsedUrl.path
#             if contentTitle is not None:
#                 # TODO: Query db for wikipediaPage if not present save to db with key as wikipediaLink
#                 # Get users username
#                 userId = c.execute("SELECT id  FROM users WHERE username = (%s)",
#                                    (thwart(request.form["username"]),))
                
#                 # Get all the wikilinks in user's wikilinks
#                 userLinks = c.execute("SELECT wikiLinks FROM userWikiLinks WHERE userId=(%s)",
#                                       (thwart(userId),))
                
#                 # Check if the link user asked for is in their list ?
#                 if wikipediaLink in userLinks:
#                     # TODO : get location where the link audio files are located in server
#                     return
#                 else:
#                     # TODO : get parsed wikipedia page, save that 
#                     return
                
#                 wikipediaPage = WikipediaParser(wikipediaLink)
#                 introText = wikipediaPage['Intro']
               

#                 GoogleTextToSpeech(url)
#             else:
#                 # TODO : Query db for the Link and get the necessary section
                
#                 return

#                 # return jsonify({'txt': txt})
#                 # return jsonify({'txt':"<p>Hello Friend</p>"})
#     except Exception as e:
#         return str(e)


@app.route('/return-files/')
def returnFiles():
    try:
        return send_file('/media/icon.svg')
    except Exception as e:
        return str(e)


@app.route('/get-file/')
def getFile():
    return send_file('/media/exam.mp3')


@app.route('/logout/')
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('homepage'))


# if __name__ == "__main__":
#     app.run(host='0.0.0.0')

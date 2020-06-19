from flask import Flask, render_template, url_for, redirect, flash, request, session, jsonify
from wtforms import Form, validators, PasswordField, TextField
from passlib.hash import sha256_crypt
from pymysql import escape_string as thwart
from functools import wraps
from urllib.parse import urlparse
import os
import gc
import logging
from logic.dbOperations import *

app = Flask(__name__, template_folder='templates' )
logging.basicConfig(filename='error.log', level=logging.DEBUG)
app.config['EXPLAIN_TEMPLATE_LOADING']= True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
db.init_app(app)


# Add a user


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
        app.logger.info("Inside homepage")
        if 'logged_in' in session:
            app.logger.info("User is logged in")
            return redirect(url_for('dashboard'))
        else:
            app.logger.info("User is NOT logged in")
            return render_template('layout/main.html')
    except Exception as e:
        return str(e)


#
@app.route('/dashboard/')
@login_required
def dashboard():
    app.logger.info("Inside dashboard")
    return render_template("/layout/dashboard.html")



@app.errorhandler(404)
def page_not_found(e):
    app.logger.info("Inside page_not_found")
    return render_template('helper_templates/404.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = ''
    try:
        app.logger.info("Inside login")
        if 'logged_in' in session:
            return redirect(url_for('dashboard'))
        elif request.method == "POST":
            app.logger.info("Inside login route %s" % db)
            app.logger.info("login request form is %s" % request.form)
            data = User.query.filter_by(username="%s" % thwart(request.form['username'])).first()

            passwd = data.password
            app.logger.info(sha256_crypt.verify(request.form['password'], passwd))
            app.logger.info("FLASK_SECRET_KEY ------> %s" % os.getenv("FLASK_SECRET_KEY"))

            if sha256_crypt.verify(request.form['password'], passwd):
                session['logged_in'] = True
                session['username'] = request.form['username']
                app.logger.info("You are now logged in")
                flash("You are now logged in")
                return redirect(url_for('dashboard'))
            else:
                app.logger.info("Invalid credentials ")
                error = "Invalid credentials, try again."

        gc.collect()
        return render_template("user_Management/login.html", error=error)

    except Exception as e:
        # flash(e)
        app.logger.error("Error occured ----> %s" % e)
        error = "Invalid credentials, try again."
        return render_template("user_Management/login.html", error=error)


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

@app.route('/register/', methods=["GET", "POST"])
def register_page():
    try:
        app.logger.info("Inside register_page  ")
        form = RegistrationForm(request.form)
        app.logger.info("username of user ---> %s" % form.username.data)
        if 'logged_in' in session:
            app.logger.info("Already logged in ")
            return redirect(url_for('dashboard'))
        elif request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.hash(thwart(str(form.password.data)))
            app.logger.info("username,email,password are : %s, %s, %s" % (username, email, password))
            foundUser = getUserDataFirst(thwart(username))
            app.logger.info("value of foundUser is  %s" % foundUser)
            if foundUser is not None:
                flash("That username is already taken, please choose another")
                return render_template('user_Management/register.html', form=form)

            else:

                createNewUser(username=thwart(username), email=thwart(email), password=password)

                flash("Thanks for registering!")
                gc.collect()
                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template("user_Management/register.html", form=form)

    except Exception as e:
        return str(e)


# app.logger.info("")
@app.route('/converttospeech/', methods=['GET', 'POST'])
@login_required
def getWiki():
    """ Receive a request to convert the clicked link to audio
        check if link is present in AllWikiLinks
            yes :
                return from there
            no  :
                get the parsed page from wikipedia class
                save that to allwikilinks list with the wikilink being path and text being the dict
                call convertospeech with necessary fragment
                get the location where this is saved
        Link in users wikilinks ?
        no : then add
        else: take user to that location

        https://en.wikipedia.org/wiki/Anarchy#Etymology
        ParseResult(scheme='https', netloc='en.wikipedia.org', path='/wiki/Anarchy',
                    params='', query='', fragment='Etymology')
    """
    try:
        app.logger.info("Inside getWiki")
        app.logger.info("request received is %s" % request.form)

        wikiLinkToBeParsed = str(request.form['wikipediaLink']).strip()
        app.logger.info(
            "wikiLink to be parsed is : %s and its type is %s" % (wikiLinkToBeParsed, type(wikiLinkToBeParsed)))
        parsedUrl = urlparse(wikiLinkToBeParsed)
        app.logger.info("parsedUrl is : %s" % str(parsedUrl))
        if parsedUrl.netloc != 'en.wikipedia.org' or parsedUrl.scheme != 'https':

            msg = "Pass a valid wikipedia url, for e.g :  https://en.wikipedia.org/wiki/Anarchy"
            return jsonify({'txt': msg, 'mediaLocation': '',"success": False,})
        else:
            path = parsedUrl.path
            fragment = parsedUrl.fragment
            username = session['username']

            newTTS = methodsForTTS(username, path, fragment)
            mediaLocation = newTTS.orchestrator() + '.mp3'
            return jsonify({'mediaLocation': mediaLocation, 'txt': 'Congrats !',"success": True,})
    except Exception as e:
        app.logger.info("error in get wiki : %s" % e)
        return str(e)


@app.route('/logout/')
@login_required
def logout():
    app.logger.info("Inside logout")
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('homepage'))



###########################################
## My utility functions will clean later ##
###########################################


# ParseResult(scheme='https', netloc='en.wikipedia.org', path='/wiki/Anarchy',
#                         params='', query='', fragment='Description')

def createTables():
    db.create_all()


def drop():
    db.drop_all()

def dc():
    drop()
    createTables()
    app.run(host="0.0.0.0", debug=True)

if __name__ == '__main__':
    with app.app_context():
        app.run(host="0.0.0.0", debug=True)
        # testTTS()
        # dc()
        # print(removeWikiLinkFromUser('qwer','_wiki_Anarchy#French Revolution (1789–1799)'))
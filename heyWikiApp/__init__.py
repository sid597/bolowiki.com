import gc
import logging
import os
from functools import wraps
from urllib.parse import urlparse
from flask_migrate import Migrate
from flask import Flask, render_template, url_for, redirect, flash, request, session, jsonify, Blueprint
from passlib.hash import sha256_crypt
from pymysql import escape_string as thwart
from wtforms import Form, validators, PasswordField, TextField

from .logic.dbOperations import *
from .translate.translator import _translate
from pprint import pprint
from .blueprints.utils import *

app = Flask(__name__, template_folder='templates')
logging.basicConfig(filename='error.log', level=logging.DEBUG)
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
db.init_app(app)
migrate = Migrate()
migrate.init_app(app, db)

from heyWikiApp.blueprints import translate, users
app.register_blueprint(translate.bp)
app.register_blueprint(users.bp)


@app.route('/')
def homepage():
    try:
        app.logger.info("Inside homepage")
        if 'logged_in' in session:
            app.logger.info("User is logged in")
            return redirect(url_for('dashboard'))
        else:
            app.logger.info("User is NOT logged in")
            return render_template('layout/homepage.html')
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

# app.logger.info("")
@app.route('/converttospeech/', methods=['GET', 'POST'])
# @login_required
@remainingCharacterLimitNotZero
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
        acceptedWikipediaUrls = {'en.wikipedia.org', 'hi.wikipedia.org'}
        getLanguageSpecificUrl = {
            'en': 'https://en.wikipedia.org',
            'hi': 'https://hi.wikipedia.org'
        }
        app.logger.info("Inside getWiki")
        app.logger.info("request received is %s" % request)
        app.logger.info("request form received is %s" % request.form)

        wikiLinkToBeParsed = str(request.form['wikipediaLink']).strip()
        articleLanguage = str(request.form['articleLanguage'])
        app.logger.info(
            "wikiLink to be parsed is : %s, artice language is %s, and its type is %s" % (wikiLinkToBeParsed, articleLanguage, type(wikiLinkToBeParsed)))
        parsedUrl = urlparse(wikiLinkToBeParsed)
        app.logger.info("parsedUrl is : %s" % str(parsedUrl))
        if parsedUrl.netloc not in acceptedWikipediaUrls or parsedUrl.scheme != 'https':

            msg = "Pass a valid wikipedia url, for e.g :  https://en.wikipedia.org/wiki/Anarchy"
            return jsonify({
                'txt': msg, 'mediaLocation':
                '', "success": False,
            })
        else:
            wikipediaNetLoc = getLanguageSpecificUrl[articleLanguage]
            path = parsedUrl.path
            fragment = parsedUrl.fragment

            if 'logged_in' in session:
                username = session['username']
                newTTS = methodsForTTS(
                    username,
                    path,
                    articleLanguage,
                    wikipediaNetLoc,
                    fragment
                )
                mediaLocation, articleFragment, articleContentsList, articleFragmentLength, articalTotalLength = newTTS.orchestrator()
                # TODO : Uncomment the following line
                # setUserRemainingLimit(username, articleFragmentLength)

                return jsonify({
                    'mediaLocation': mediaLocation + '.mp3',
                    'txt': articleFragment,
                    "success": True,
                    'articleContents': articleContentsList,
                    'articleFragmentLength': articleFragmentLength,
                    'articalTotalLength': articalTotalLength, 
                })
            else:
                username = 'UserNotLoggedIn'
                fragment = ''
                newTTS = methodsForTTS(
                    username,
                    path,
                    articleLanguage,
                    wikipediaNetLoc,
                    fragment
                )
                mediaLocation, articleFragment, articleContentsList, articleFragmentLength, articalTotalLength = newTTS.orchestrator()
                return jsonify({
                    'mediaLocation': mediaLocation + '.mp3',
                    'txt': articleFragment,
                    "success": True,
                    'articleContents': '',
                    'articleFragmentLength': articleFragmentLength,
                    'articalTotalLength': articalTotalLength
                })
    except Exception as e:
        app.logger.info("error in get wiki : %s" % e)
        return str(e)
    
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

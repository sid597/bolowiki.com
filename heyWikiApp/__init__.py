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

from .dbOperations import *
from pprint import pprint

app = Flask(__name__, template_folder='templates')
logging.basicConfig(filename='error.log', level=logging.DEBUG)
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
db.init_app(app)
migrate = Migrate()
migrate.init_app(app, db)

from .Users.routes import users_bp
from .Translate.routes import translate_bp
from .text_to_speech.routes import textToSpeech_bp
from .main.routes import main_bp
app.register_blueprint(main_bp)
app.register_blueprint(translate_bp)
app.register_blueprint(users_bp)
app.register_blueprint(textToSpeech_bp)




    
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

# Python Packages
import gc

# External packages
from flask import render_template, url_for, redirect, flash, request, session, jsonify, Blueprint
from passlib.hash import sha256_crypt
from pymysql import escape_string as thwart
from wtforms import Form, validators, PasswordField, TextField
from flask import  current_app as app

# Local packages
from ..dbOperations import  getUserDataFirst, createNewUser, getUserRemainingLimit
from ..utils import login_required, remainingCharacterLimitNotZero, getRemainingLimit


users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/login/', methods=['GET', 'POST'])
def login():
    error = ''
    try:
        print("Inside login")
        if 'logged_in' in session:
            return redirect(url_for('main_bp.homepage'))
        elif request.method == "POST":
            print("Inside login route ")
            print("request  is %s" % request)

            print("login request form is %s" % request.form)
            print('thwarted username is %s' %
                            thwart(request.form['username']))
            user = getUserDataFirst(thwart(request.form['username']))
            print('user info received from db is %s' % user.password)
            UserPassword = user.password

            print(sha256_crypt.verify(
                request.form['password'], UserPassword))

            if sha256_crypt.verify(request.form['password'], UserPassword):
                session['logged_in'] = True
                session['username'] = request.form['username']
                print("You are now logged in")
                flash("You are now logged in")
                return redirect(url_for('main_bp.dashboard'))
            else:
                print("Invalid credentials ")
                error = "Invalid credentials, try again."

        gc.collect()
        return render_template("user_Management/login.html", error=error)

    except Exception as e:
        # flash(e)
        # app.logger.error("Error occured ----> %s" % e)
        error = "Invalid credentials, try again."
        return render_template("user_Management/login.html", error=error)

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm',
                           message='Passwords must match'
                           )
    ])
    confirm = PasswordField('Repeat Password')


@users_bp.route('/register/', methods=["GET", "POST"])
def register_page():
    try:
        # print("Inside register_page  ")
        form = RegistrationForm(request.form)
        # print("username of user ---> %s" % form.username.data)
        if 'logged_in' in session:
            # print("Already logged in ")
            return redirect(url_for('main_bp.dashboard'))
        elif request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.hash(thwart(str(form.password.data)))
            # print("username,email,password are : %s, %s, %s"
                            # % (username, email, password))
            foundUser = getUserDataFirst(thwart(username))
            # print("value of foundUser is  %s" % foundUser)
            if foundUser is not None:
                flash("That username is already taken, please choose another")
                return render_template('user_Management/register.html', form=form)

            else:
                createNewUser(
                    username=thwart(username),
                    email=thwart(email),
                    password=password
                )
                flash("Thanks for registering!")
                gc.collect()
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('main_bp.dashboard'))
        return render_template("user_Management/register.html", form=form)
    except Exception as e:
        return str(e)
   
@users_bp.route('/logout/')
@login_required
def logout():
    # print("Inside logout")
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('main_bp.homepage'))
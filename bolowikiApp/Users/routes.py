# Python Packages
import gc

# External packages
from flask import current_app as app
from flask import render_template, url_for, redirect, flash, request, session, Blueprint
from passlib.hash import sha256_crypt
from pymysql import escape_string as thwart
from wtforms import Form, validators, PasswordField, TextField


# Local packages
from ..dbOperations import getUserDataFirst, createNewUser
from ..utils import login_required

users_bp = Blueprint('users_bp', __name__, template_folder='html_templates')


@users_bp.route('/login/', methods=['GET', 'POST'])
def login():
    error = ''
    try:
        if 'logged_in' in session:
            return redirect(url_for('main_bp.homepage'))
        user = getUserDataFirst(thwart(request.form['username']))
        UserPassword = user.password
        if sha256_crypt.verify(request.form['password'], UserPassword):
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash("You are now logged in")
            return redirect(url_for('main_bp.dashboard'))
        error = "Invalid credentials, try again."
        gc.collect()
        return render_template("login.html", error=error)

    except:
        # flash(e)
        app.logger.error("Error occured ----> %s" % Exception)
        error = "Invalid credentials, try again."
        return render_template("login.html", error=error)


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm',
                           message='Passwords must match'
                           )
    ])
    confirm = PasswordField('Confirm Password')


@users_bp.route('/register/', methods=["GET", "POST"])
def register_page():
    try:
        # print("Inside register_page  ")
        form = RegistrationForm(request.form)
        # print("username of user ---> %s" % form.username.data)
        if 'logged_in' in session:
            # print("Already logged in ")
            return redirect(url_for('main_bp.dashboard'))
        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.hash(thwart(str(form.password.data)))
            # print("username,email,password are : %s, %s, %s"
            # % (username, email, password))
            foundUser = getUserDataFirst(thwart(username))
            # print("value of foundUser is  %s" % foundUser)
            if foundUser is not None:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

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
        return render_template("register.html", form=form)
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

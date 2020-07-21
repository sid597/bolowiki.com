# Python Packages
from functools import wraps

# External Packages
from flask import session, flash, redirect, url_for

# Local Packages
from .dbOperations import getUserRemainingLimit

# Wrappers
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('main_bp.main.login'))
    return wrap

def remainingCharacterLimitNotZero(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            remainingLimit = getRemainingLimit()
            if remainingLimit > 0:
                return f(*args, **kwargs)
        flash("Your limit for voice conversion is over contact siddharthdv77@gmail.com to upgrade.")
    return wrap

def getRemainingLimit():
    username = session['username']
    remainingLimit = getUserRemainingLimit(username)
    return remainingLimit
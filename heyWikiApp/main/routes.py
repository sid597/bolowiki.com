# External packages
from flask import session, redirect, render_template, url_for, Blueprint
from ..utils import login_required

main_bp = Blueprint('main_bp', __name__)


@main_bp.route('/')
def homepage():
    try:
        # app.logger.info("Inside homepage")
        if 'logged_in' in session:
            # app.logger.info("User is logged in")
            return redirect(url_for('main_bp.dashboard'))
        else:
            # app.logger.info("User is NOT logged in")
            return render_template('layout/homepage.html')
    except Exception as e:
        return str(e)



@main_bp.route('/dashboard/')
@login_required
def dashboard():
    # app.logger.info("Inside dashboard")
    return render_template("/layout/dashboard.html")


@main_bp.errorhandler(404)
def page_not_found(e):
    # app.logger.info("Inside page_not_found")
    return render_template('helper_templates/404.html')

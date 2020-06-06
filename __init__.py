from flask import Flask, render_template, url_for, redirect, flash, request, session, send_file, jsonify
from wtforms import Form, BooleanField, validators, PasswordField, TextField
from dbconnect import connection
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from functools import wraps
from content_management import Content
import gc
from google.cloud import texttospeech
import os

app = Flask(__name__)
#app.secret_key=os.environ.get("FLASK_APP_SECRET_KEY")
#app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap


@app.route('/converttospeech/', methods=['GET', 'POST'])
@login_required
def convertToSpeech():
    try:
        txt = request.form['textforspeech']
        GoogleTextToSpeech(txt)
        return jsonify({'txt': txt})
        # return jsonify({'txt':"<p>Hello Friend</p>"})
    except Exception as e:
        return str(e)


def GoogleTextToSpeech(textToConvert, saveLocation='/static/converts/'):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=textToConvert)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open("output.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        # print('Audio content written to file "output.mp3"')


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



@app.route('/logout/')
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('homepage'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = ''
    try:
        c, conn = connection()
        if 'logged_in' in session:
            return redirect(url_for('dashboard'))
        elif request.method == "POST":
            data = c.execute("SELECT * FROM users WHERE username = (%s)",
                             (thwart(request.form["username"]),))

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

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(username),))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))

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


@app.route('/return-files/')
def returnFiles():
    try:
        return send_file('/media/icon.svg')
    except Exception as e:
        return str(e)


@app.route('/get-file/')
def getFile():
    return send_file('/media/exam.mp3')


#if __name__ == "__main__":
#     app.run(host='0.0.0.0')



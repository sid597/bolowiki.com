from __init__ import app
import os


app.secret_key = os.getenv("FLASK_APP_SECRET_KEY")

if __name__ == "__main__":
    app.logger.info("Inside wsgi")
    app.logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    app.logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    app.run()

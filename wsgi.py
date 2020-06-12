from __init__ import app
import os

# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# print( app.secret_key)
# a = os.environ.get("FLASH_APP_SECRET_KEY")
app.secret_key = os.getenv("FLASK_APP_SECRET_KEY")
# print(app.secret_key)
if __name__ == "__main__":
    app.run()

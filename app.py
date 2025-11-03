from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.models import *
def create_app():
    app  = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_db.sqlite3"
    db.init_app(app)
    app.app_context().push()
    return app


app = create_app()

from backend.routes import *
from backend.create_inital_data import *

if "__main__"==__name__:
    app.run(debug=True)
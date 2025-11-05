from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.models import *
from flask_login import LoginManager
def create_app():
    app  = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_db.sqlite3"
    db.init_app(app)
    app.app_context().push()
    app.config['SECRET_KEY'] = 'supersecretkey'
    login_manager = LoginManager(app)
    @login_manager.user_loader
    def load_user(email):
        user = db.session.query(Customer).filter_by(email=email).first()  or \
                db.session.query(Admin).filter_by(email=email).first() or \
                db.session.query(Professional).filter_by(email=email).first()
        return user

    return app


app = create_app()

from backend.routes import *
from backend.create_inital_data import *

if "__main__"==__name__:
    app.run(debug=True)
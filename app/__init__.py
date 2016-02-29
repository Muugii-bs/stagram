from flask import Flask, Request
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.login as flask_login
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

from app import views, models
from app.models import User
import db_utils

def init_db():
	db_utils.db_clean()
	db.create_all(app=app)
	db_utils.db_create_default(db)

if __name__ == '__main__':
	app.run()

@login_manager.user_loader 
def load_user(id):
	return User.query.get(int(id))


from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from flask_ngrok import run_with_ngrok
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = '444529d5f8ba707b7da4e4e0c58a5555'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apihashtag.db'
database  = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'homepage'


from hashtag_processo_seletivo import routes 
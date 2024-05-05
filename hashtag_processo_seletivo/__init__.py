from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from flask_ngrok import run_with_ngrok
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '444529d5f8ba707b7da4e4e0c58a5555'
if os.getenv("DATABASE_URL"): 
    URL_DB = os.getenv('DATABASE_URL')
    nova_URL = URL_DB.replace('postgres://', 'postgresql://')
    app.config['SQLALCHEMY_DATABASE_URI'] = nova_URL
else: 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apihashtag.db'
database  = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'homepage'

from hashtag_processo_seletivo import models
engine=sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector=sqlalchemy.inspect(engine)
if not inspector.has_table("user"):
    with app.app_context():
        database.drop_all()
        database.create_all()

else:

    pass



from hashtag_processo_seletivo import routes 
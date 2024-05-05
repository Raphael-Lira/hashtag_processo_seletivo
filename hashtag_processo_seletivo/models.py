from hashtag_processo_seletivo  import  database, login_manager
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id_usuario ):
    return User.query.get(int(id_usuario))


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, unique=True, nullable=False)
    senha = database.Column(database.String, nullable=False)
    token = database.Column(database.String, nullable=False)  



class Webhook(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    data = database.Column(database.Date, nullable=False)
    nome = database.Column(database.String(100), nullable=False)
    email = database.Column(database.String(100), nullable=False)
    status = database.Column(database.String(100), nullable=False)
    valor = database.Column(database.Float, nullable=False)
    forma_pagamento = database.Column(database.String(100), nullable=False)
    parcelas = database.Column(database.Integer, nullable=False)
    tratativa = database.Column(database.String(100), nullable=True)
   
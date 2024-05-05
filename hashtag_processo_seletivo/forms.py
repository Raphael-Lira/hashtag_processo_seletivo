from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from wtforms.validators import Email as EmailValidator
from wtforms import RadioField
from hashtag_processo_seletivo.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Nome', validators=[DataRequired(), Length(6, 20)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação senha', validators=[DataRequired(), EqualTo('senha')])
    token = PasswordField('Token', validators=[DataRequired()])
    submit = SubmitField('Criar Conta')
    def validate_email(self, email):
        usuario = User.query.filter_by(email=email.data).first()
        if usuario: 
            return ValidationError('E-mail já cadastrado ! ')
from flask import render_template, url_for, redirect, request, session
from hashtag_processo_seletivo import app, database, bcrypt
from hashtag_processo_seletivo.models import Webhook,User
from hashtag_processo_seletivo.forms import RegisterForm, LoginForm
from datetime import datetime
from flask_login import login_required, login_user, logout_user, current_user
from wtforms.validators import Email
from sqlalchemy import or_
from sqlalchemy import desc

@app.route('/', methods=['GET', 'POST'])
def homepage():
    form_login = LoginForm()
    error_message = None
    if form_login.validate_on_submit():

        usuario = User.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)

            return redirect(url_for('painel', usuario=usuario.username))
        else:
            if usuario is None :
                error_message = 'Email não cadastrado. Por favor, verifique o email digitado.'
            else:
                error_message = 'Senha inválida. Por favor, tente novamente.'
    return render_template('home.html', form=form_login, error_message=error_message)


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True, silent=True)
    if not data:
        data = request.form.to_dict(flat=True)

    app.logger.info('Dados do webhook recebidos: %s', data)

    nome = data.get('nome')
    email = data.get('email')
    status = data.get('status')
    valor = data.get('valor')
    forma_pagamento = data.get('forma_pagamento')
    parcelas = data.get('parcelas')

    # Processamento do pagamento
    tratativa = None
    if status == 'aprovado':
        print(f"Liberar acesso do e-mail: {email}")
        tratativa = 'acesso liberado, seja bem vindo ! '
    elif status == 'recusado':
        print(f"Pagamento recusado do e-mail : {email}")
        tratativa = 'Pagamento recusado'
    elif status == 'reembolsado':
        print(f"Acesso revogado do e-mail : {email}")
        tratativa = 'Acesso revogado'

    # Salvar os dados no banco de dados
    webhook = Webhook(data=datetime.now(), nome=nome, email=email, status=status, valor=valor, forma_pagamento=forma_pagamento, parcelas=parcelas, tratativa=tratativa)
    database.session.add(webhook)
    database.session.commit()

    app.logger.info('Webhook recebido e processado com sucesso')
    return 'Webhook recebido e processado com sucesso', 200


@app.route('/registrar', methods=['GET', 'POST'])
def criar_conta():
    form_registrar_conta = RegisterForm()
    error_message = None
    if form_registrar_conta.validate_on_submit():
        if form_registrar_conta.token.data == 'uhdfaAADF123':
            senha_crypt = bcrypt.generate_password_hash(form_registrar_conta.senha.data)
            print(senha_crypt)
            usuario = User(username=form_registrar_conta.username.data, email=form_registrar_conta.email.data,
                            senha=senha_crypt, token=form_registrar_conta.token.data)
            database.session.add(usuario)
            database.session.commit()
            login_user(usuario, remember=True)
            return redirect(url_for('painel', usuario=usuario.username))
        else:
            error_message = 'Token inválido'
    else:  # Se o formulário não foi submetido
        if form_registrar_conta.senha.data != form_registrar_conta.confirmacao_senha.data:
            error_message = 'As senhas não coincidem. Por favor, tente novamente.'
    return render_template('criar_conta.html', form=form_registrar_conta, error_message=error_message )


@app.route('/painel/<usuario>', methods=['GET', 'POST'])
@login_required 
def painel(usuario):
    page = request.args.get('page', 1, type=int)  # Pega o número da página da URL
    per_page = 5  # Define o número de registros por página
    search_term = request.args.get('search_term', '')

    # Ordena os registros em ordem decrescente pelo índice
    webhooks = Webhook.query.filter(
        or_(Webhook.nome.ilike(f'%{search_term}%'), Webhook.email.ilike(f'%{search_term}%'))
    ).order_by(desc(Webhook.id)).paginate(page=page, per_page=per_page)

    return render_template('painel.html', usuario=usuario, webhooks=webhooks)


@app.route('/logout')
@login_required 
def logout(): 
    logout_user()
    return redirect(url_for('homepage'))
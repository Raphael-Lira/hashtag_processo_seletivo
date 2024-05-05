from hashtag_processo_seletivo import database, app
from hashtag_processo_seletivo.models import User, Webhook


with app.app_context():
    database.create_all()
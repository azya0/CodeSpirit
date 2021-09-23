from data.__all_models import User
import flask
import json
import re
from data import db_session

blueprint = flask.Blueprint(
    'system', __name__,
    template_folder='templates',
    static_folder="static"
)


def valid(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True
    return False


@blueprint.route('/system/email/<string:user_email>', methods=['GET', 'POST'])
def is_email_used(user_email):
    session = db_session.create_session()
    if session.query(User).filter(User.email == user_email).first():
        return 'used'
    return 'unused'


@blueprint.route('/system/valid_email/<string:user_email>', methods=['GET', 'POST'])
def valid_email(user_email):
    if valid(user_email):
        return 'true'
    return 'false'

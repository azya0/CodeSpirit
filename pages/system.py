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


def valid_email_(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True
    return False


def valid_login_(login):
    if any([elm in login for elm in ' !@"#№$;%^:&?*()-+={}[]./\'<>~']) and len(login) < 3:
        return False
    return True


@blueprint.route('/system/email/<string:user_email>', methods=['GET', 'POST'])
def is_email_used(user_email):
    session = db_session.create_session()
    if session.query(User).filter(User.email == user_email).first():
        return 'used'
    return 'unused'


@blueprint.route('/system/valid_email/<string:user_email>', methods=['GET', 'POST'])
def valid_email(user_email):
    if valid_email_(user_email):
        return 'true'
    return 'false'


@blueprint.route('/system/login/<string:user_login>', methods=['GET', 'POST'])
def is_login_used(user_login):
    session = db_session.create_session()
    if session.query(User).filter(User.name == user_login).first():
        return 'used'
    return 'unused'


@blueprint.route('/system/valid_login/<string:user_login>', methods=['GET', 'POST'])
def valid_login(user_login):
    if valid_login_(user_login):
        return 'true'
    return 'false'

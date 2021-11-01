from flask_login import LoginManager, current_user
from flask import Flask, redirect
from data import db_session
from data.__all_models import User
from pages import home, q_and_a, authentication, chats
import configparser

app = Flask(__name__, static_folder="static")
config = configparser.ConfigParser()
config.read('static/config.ini')
app.config['SECRET_KEY'] = config['App']['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = config['App']['UPLOAD_FOLDER']
app.config['MAX_CONTENT_LENGTH'] = int(config['App']['MAX_CONTENT_LENGTH'])
app.config['last_uploaded_file'] = config['App']['last_file_way']
app.add_url_rule("/uploads/<name>", endpoint="download_file", build_only=True)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.errorhandler(401)
def internal_error(error):
    return redirect('/login')


def main():
    db_session.global_init("db/database.db")
    app.run()


if __name__ == '__main__':
    app.register_blueprint(home.blueprint)
    app.register_blueprint(authentication.blueprint)
    app.register_blueprint(chats.blueprint)
    app.register_blueprint(q_and_a.blueprint)
    main()

from flask_login import LoginManager, current_user
from flask import Flask, redirect
from data import db_session
from data.__all_models import User
from pages import home, authentication

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = 'piuhPIDFUSHG<-I\'llNeverBeAloneAgain?->KOJDSkfoijds'
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(401)
def user_unauthorized(error):
    return redirect("/login")


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


def main():
    db_session.global_init("db/database.db")
    app.run()


if __name__ == '__main__':
    app.register_blueprint(home.blueprint)
    app.register_blueprint(authentication.blueprint)
    main()

from flask import Flask
from data import db_session
from pages import main_page

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = 'piuhPIDFUSHG<-I\'llNeverBeAloneAgain?->KOJDSkfoijds'


def main():
    db_session.global_init("db/database.db")
    app.run()


if __name__ == '__main__':
    app.register_blueprint(main_page.blueprint)
    main()
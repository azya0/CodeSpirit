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

'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet"
          href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
          integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh"
          crossorigin="anonymous">
    <link href="{{ url_for('static', filename='own.css') }}" rel="stylesheet"/>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js"></script>
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <title>Title</title>
</head>
<body>
<svg display="none">
    <symbol id="logo" viewBox="0 0 512 512">
        <g fill="#fff"><path d="m266 223.1h-54.9l-17.2-29.8h89.3l26.1-45.3h-147.6c-9.4 0-18.3 5-22.9 13.3-4.8 8.3-4.8 18.3 0 26.6l94.1 163.1c7.4 12.6 23.7 16.8 36.4 9.4 3.9-2.4 7.2-5.4 9.4-9.4l3-5.4-43.3-75.1z"/><path d="m373.2 161.3c-4.8-8.3-13.5-13.3-22.9-13.3h-6.5l-70.8 122.4 25.9 45.3 74-128.1c5.1-8 5.1-18 .3-26.3z"/></g>
    </symbol>
</svg>
    <nav class="navbar navbar-expand-sm navbar-dark bg-dark main-navbar d-flex justify-content-center">
        <div class="main-side d-inline-flex align-items-center">
            <div class="d-inline-flex align-items-center my-1">
                <svg class="logo" width="60" height="60">
                    <use xlink:href="#logo"></use>
                </svg>
                <h3 class="logo">Dionysus</h3>
            </div>
            <div class="ml-2">
                <input class="main-search-box" type="search" placeholder="Поиск">
            </div>
            <div class="ml-3 collapse navbar-collapse" id="links">
                <ul class="navbar-nav">
                    <li class="nav-item active"><a class="nav-link active" href="#">Main</a></li>
                    <li class="nav-item active"><a class="nav-link" href="#">Someshit</a></li>
                    <li class="nav-item active"><a class="nav-link" href="#">Someshit</a></li>
                    <li class="nav-item active"><a class="nav-link" href="#">Someshit</a></li>
                </ul>
            </div>
        </div>
    </nav>




    <main role="main" class="container">
    {% block content %}{% endblock %}
    </main>
</body>
</html>
'''
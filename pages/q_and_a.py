from flask_login import login_required, current_user
from data.__all_models import *
from data.forms import *
from flask import render_template, redirect
import datetime
import flask

from data import db_session

blueprint = flask.Blueprint(
    'q_and_a', __name__,
    template_folder='templates',
    static_folder="static"
)


def mini_qaa_text(string: str) -> str:
    return string.split('\n')[0][:401].strip() + ('...' if len(string.split('\n')[0][:251].strip()) != len(string) else '')


@blueprint.route('/q&a', methods=['GET', 'POST'])
@login_required
def main_page():
    session = db_session.create_session()
    form = QAAForm()
    answer_form = AnswerForm()
    data = {
        'session': session,
        'files': session.query(File),
        'answers': session.query(Answer),
        'likes': session.query(Like),
        'questions': sorted(session.query(QAA).all(), key=lambda x: x.datetime, reverse=True),
        'form': form,
        'answer_form': answer_form,
        'User': User,
        'File': File,
        'Like': Like,
        'Answer': Answer,
        'current_user': current_user,
        'enumerate': enumerate,
        'qaa_text': mini_qaa_text,
        'len': len,
        'author': lambda x: session.query(User).get(x)
    }
    return render_template("qaa.html", **data)


@blueprint.route('/q&a/form', methods=['GET', 'POST'])
@login_required
def qaa_form():
    form = QAAForm()
    if form.validate_on_submit():
        qaa, session = QAA(), db_session.create_session()
        qaa.author = current_user.id
        qaa.title = form.title.data.strip()
        qaa.text = form.text.data.strip()
        qaa.datetime = datetime.datetime.now()
        qaa.tags = form.tags.data
        session.add(qaa)
        session.commit()
        return redirect('/q&a')

    data = {
        'form': form
    }
    return render_template("qaa-form.html", **data)

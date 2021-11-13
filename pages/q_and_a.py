from flask_login import login_required, current_user
from data.__all_models import *
from data.forms import *
from flask import render_template, redirect
from random import randint, choice
import datetime
import flask

from data import db_session

blueprint = flask.Blueprint(
    'q_and_a', __name__,
    template_folder='templates',
    static_folder="static"
)


def mini_qaa_text(string: str) -> str:
    string = string.replace('\n', ' ').strip()[:401].strip()
    for key in ('\\```', '```'):
        string = string.replace(key, '')
    return string


def replace_sims(string: str) -> str:
    result = re.findall('```.*?```', string)
    for elm in result:
        string.replace(elm, elm[3:-3])
    return string


@blueprint.route('/q&a', methods=['GET', 'POST'])
@login_required
def main_page():
    session = db_session.create_session()
    form = QAAForm()
    data = {
        'session': session,
        'files': session.query(File),
        'answers': session.query(Answer),
        'likes': session.query(Like),
        'questions': sorted(session.query(QAA).all(), key=lambda x: x.datetime, reverse=True),
        'form': form,
        'User': User,
        'File': File,
        'Like': Like,
        'current_user': current_user,
        'gradient': lambda: f'linear-gradient({randint(30, 90)}deg, rgba({randint(50, 180)},20,{randint(0, 60)},1)'
                            f'0%, rgba({randint(50, 180)},{randint(80, 200)},{randint(50, 180)},1) 28%,'
                            f'rgba({randint(111, 180)},{randint(50, 200)},{randint(150, 180)},1) 72%, rgba({randint(0, 100)},{randint(50, 180)},{randint(100, 200)},{randint(0, 100)}) 100%);',
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
        qaa.title = form.title.data.strip().capitalize()
        qaa.text = form.text.data.strip()
        qaa.datetime = datetime.datetime.now()
        qaa.tags = ' '.join(map(str.strip, form.tags.data.split()))
        session.add(qaa)
        session.commit()
        return redirect('/q&a')

    data = {
        'form': form
    }
    return render_template("qaa-form.html", **data)


@blueprint.route('/q&a/<int:id>', methods=['GET', 'POST'])
@login_required
def qaa_a_page(id):
    form, session = AnswerForm(), db_session.create_session()
    question = session.query(QAA).get(id)
    data = {
        'id': id,
        'session': session,
        'files': session.query(File),
        'answers': session.query(Answer),
        'is_liked': session.query(Like).filter(Like.author == current_user.id).filter(
            Like.type == 'QAA').filter(Like.obj_id == id).filter(Like.dislike == False).first(),
        'is_disliked': session.query(Like).filter(Like.author == current_user.id).filter(
            Like.type == 'QAA').filter(Like.obj_id == id).filter(Like.dislike == True).first(),
        'question': question,
        'form': form,
        'User': User,
        'File': File,
        'Like': Like,
        'Answer': Answer,
        'enumerate': enumerate
    }
    question.views += 1
    session.commit()
    return render_template("qaa-q-page.html", **data)


@blueprint.route('/like/qaa_post/<int:id>/<int:like>', methods=['GET'])
@login_required
def like_qaa_post(id, like):
    def refresh_rating(reverse=False, double=False):
        rate_ = rate * 2 if double else rate
        qaa.rating += (-rate_ if reverse else rate_)
        data['rating'] = qaa.rating

    session = db_session.create_session()
    qaa = session.query(QAA).get(id)
    rate = (1 if like else -1)

    data = {
        'result': 'success',
        'rating': qaa.rating,
        'cancel': 'False',
        'double': 'False'
    }

    like_obj = session.query(Like).filter(Like.author == current_user.id).filter(
        Like.type == 'QAA').filter(Like.obj_id == id).first()

    if not like_obj:
        like_obj = Like()
        like_obj.author = current_user.id
        like_obj.type = 'QAA'
        like_obj.obj_id = id
        like_obj.dislike = not bool(like)
        like_obj.datetime = datetime.datetime.now()
        session.add(like_obj)
        refresh_rating()
        qaa.rated += 1
    else:
        if not (like_obj.dislike != bool(like)):
            like_obj.dislike = not like_obj.dislike
            refresh_rating(double=True)
            data['double'] = 'True'
        else:
            session.delete(like_obj)
            qaa.rated -= 1
            refresh_rating(reverse=True)
        data['cancel'] = 'True'
    session.commit()
    return flask.jsonify(data)

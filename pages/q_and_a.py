from flask_login import login_required, current_user
from data.__all_models import *
from data.forms import *
from flask import render_template, redirect
from random import randint, choice
from pages.home import format_string
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


def answered(qaa_id):
    session = db_session.create_session()
    return session.query(Answer).filter(Answer.qaa_id == qaa_id).filter(Answer.right_answer == True).first()


@blueprint.route('/q&a', methods=['GET', 'POST'])
@login_required
def main_page():
    session = db_session.create_session()
    form = AnswerForm()
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
        'gradient': lambda: f'linear-gradient({randint(40, 160)}deg, rgba({randint(80, 255)},50,{randint(56, 110)},1)'
                            f'0%, rgba({randint(15, 100)},{randint(0, 107)},{randint(170, 250)},1) 28%,'
                            f'rgba({randint(151, 200)},{randint(50, 140)},{randint(10, 56)},1) 72%);',
        'enumerate': enumerate,
        'qaa_text': mini_qaa_text,
        'len': len,
        'author': lambda x: session.query(User).get(x),
        'answ_count': lambda x: len(session.query(Answer).filter(Answer.qaa_id == x).all()),
        'answered': answered
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
    session = db_session.create_session()
    comment_form = QaaCommentForm()
    answer_form = AnswerForm()
    question = session.query(QAA).get(id)
    data = {
        'id': id,
        'session': session,
        'files': session.query(File),
        'answers': session.query(Answer).filter(Answer.qaa_id == id).all(),
        'comments': session.query(QaaComment),
        'is_liked': session.query(Like).filter(Like.author == current_user.id).filter(
            Like.type == 'QAA').filter(Like.obj_id == id).filter(Like.dislike == False).first(),
        'is_disliked': session.query(Like).filter(Like.author == current_user.id).filter(
            Like.type == 'QAA').filter(Like.obj_id == id).filter(Like.dislike == True).first(),
        'is_qaa_comment_liked': lambda x: session.query(Like).filter(Like.author == current_user.id).filter(
            Like.obj_id == x).filter(Like.type == 'Answer').filter(Like.dislike == False).first(),
        'is_qaa_comment_disliked': lambda x: session.query(Like).filter(Like.author == current_user.id).filter(
            Like.obj_id == x).filter(Like.type == 'Answer').filter(Like.dislike == True).first(),
        'question': question,
        'comment_form': comment_form,
        'answer_form': answer_form,
        'User': User,
        'File': File,
        'Like': Like,
        'Answer': Answer,
        'QaaComment': QaaComment,
        'enumerate': enumerate,
        'len': len,
        'str': str,
        'get_user': lambda x: session.query(User).get(x),
        'answered': answered
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
    else:
        if not (like_obj.dislike != bool(like)):
            like_obj.dislike = not like_obj.dislike
            refresh_rating(double=True)
            data['double'] = 'True'
        else:
            session.delete(like_obj)
            refresh_rating(reverse=True)
        data['cancel'] = 'True'
    session.commit()
    return flask.jsonify(data)


@blueprint.route('/like/qaa_comment/<int:id>/<int:like>', methods=['GET'])
@login_required
def like_qaa_comment(id, like):
    def refresh_rating(reverse=False, double=False):
        rate_ = rate * 2 if double else rate
        qaa.rating += (-rate_ if reverse else rate_)
        data['rating'] = qaa.rating

    session = db_session.create_session()
    qaa = session.query(Answer).get(id)
    rate = (1 if like else -1)

    data = {
        'result': 'success',
        'rating': qaa.rating,
        'cancel': 'False',
        'double': 'False'
    }

    like_obj = session.query(Like).filter(Like.author == current_user.id).filter(
        Like.type == 'Answer').filter(Like.obj_id == id).first()

    if not like_obj:
        like_obj = Like()
        like_obj.author = current_user.id
        like_obj.type = 'Answer'
        like_obj.obj_id = id
        like_obj.dislike = not bool(like)
        like_obj.datetime = datetime.datetime.now()
        session.add(like_obj)
        refresh_rating()
    else:
        if not (like_obj.dislike != bool(like)):
            like_obj.dislike = not like_obj.dislike
            refresh_rating(double=True)
            data['double'] = 'True'
        else:
            session.delete(like_obj)
            refresh_rating(reverse=True)
        data['cancel'] = 'True'
    session.commit()
    return flask.jsonify(data)


@blueprint.route('/add_answer/<int:id>', methods=['GET', 'POST'])
@login_required
def add_answer(id):
    try:
        form = AnswerForm()
        if form.validate_on_submit():
            answer, session = Answer(), db_session.create_session()
            answer.text = format_string(form.text.data)
            if not answer.text:
                return flask.redirect('/')
            answer.author = current_user.id
            answer.qaa_id = id
            answer.datetime = datetime.datetime.now()
            session.add(answer)
            session.commit()
            qaa = session.query(QAA).get(answer.qaa_id)
            return flask.jsonify({
                'result': 'success',
                'id': answer.id,
                'right_answer': answer.right_answer,
                'author': answer.author,
                'q_id': answer.qaa_id,
                'name': session.query(User).get(answer.author).name,
                'rating': answer.rating,
                'text': answer.text,
                'author_of_qaa': qaa.author == current_user.id and not session.query(Answer).filter(
                    Answer.qaa_id == qaa.id).filter(Answer.right_answer == True).first(),
            })
    except BaseException as exception:
        return flask.jsonify({'result': f'error {exception}'})
    return flask.jsonify({'result': 'the minimum answer length is 25 characters'})


@blueprint.route('/add_qaa_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def add_qaa_comment(id):
    try:
        form = QaaCommentForm()
        if form.validate_on_submit():
            comment, session = QaaComment(), db_session.create_session()
            comment.text = format_string(form.text.data)
            if not comment.text:
                return flask.redirect('/')
            comment.author = current_user.id
            comment.answer_id = id
            comment.datetime = datetime.datetime.now()
            session.add(comment)
            session.commit()
            return flask.jsonify({
                    'result': 'success',
                    'text': comment.text.strip().replace('\n\n', '\n'),
                    'author': comment.author,
                    'datetime': comment.datetime.strftime("%a, %d %b %Y %H:%M:%S GMT"),
                    'user': session.query(User).get(comment.author).name
                })
    except BaseException as exception:
        return flask.jsonify({'result': f'error: {exception}'})
    return flask.jsonify({'result': '250 characters maximum'})


@blueprint.route('/mark_as_right/<int:question_id>/<int:answer_id>', methods=['GET'])
@login_required
def mark_as_right(question_id, answer_id):
    session = db_session.create_session()
    question, answer = session.query(QAA).get(question_id), session.query(Answer).get(answer_id)
    if current_user.id != question.author:
        return flask.jsonify({'result': 'user is not author'})
    if not answer or answer.qaa_id != question_id:
        return flask.jsonify({'result': 'error: no such answer'})
    if not question:
        return flask.jsonify({'result': 'error: no such question'})
    if answered(question.id) and not answer.right_answer:
        return flask.jsonify({'result': 'error: already answered'})
    already = answer.right_answer
    answer.right_answer = not already
    session.commit()
    return flask.jsonify({'result': 'success', 'canceled': f'{already}'})

from flask_login import login_required, current_user
from data.request_tools import *
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
        'question_rating': get_QaaPost_rating,
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
    notifications, unwatched_notifications = get_notification()
    data['notifications'] = list(notifications)
    data['unwatched'] = unwatched_notifications
    data['get_user'] = lambda x: session.query(User).get(x)
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
    notifications, unwatched_notifications = get_notification()
    data['notifications'] = list(notifications)
    data['unwatched'] = unwatched_notifications
    session = db_session.create_session()
    data['get_user'] = lambda x: session.query(User).get(x)
    return render_template("qaa-form.html", **data)


@blueprint.route('/q&a/<int:id>', methods=['GET', 'POST'])
@login_required
def qaa_a_page(id):
    def is_liked(_id, _type, disliked=False):
        return session.query(Like).filter(Like.author == current_user.id).filter(
            Like.obj_id == get_LikeObj_id(_id, _type)).filter(Like.dislike == disliked).first()

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
        'is_liked': is_liked(id, 'QAA'),
        'is_disliked': is_liked(id, 'QAA', True),
        'is_qaa_comment_liked': lambda x: is_liked(x, 'Answer'),
        'is_qaa_comment_disliked': lambda x: is_liked(x, 'Answer', True),
        'question_rating': get_QaaPost_rating,
        'question': question,
        'comment_form': comment_form,
        'answer_form': answer_form,
        'User': User,
        'File': File,
        'Like': Like,
        'Answer': Answer,
        'AnswerRating': get_Answer_rating,
        'QaaComment': QaaComment,
        'enumerate': enumerate,
        'len': len,
        'str': str,
        'get_user': lambda x: session.query(User).get(x),
        'answered': answered
    }
    question.views += 1
    session.commit()
    notifications, unwatched_notifications = get_notification()
    data['notifications'] = list(notifications)
    data['unwatched'] = unwatched_notifications
    return render_template("qaa-q-page.html", **data)


@blueprint.route('/like/qaa_post/<int:id>/<int:liked>', methods=['GET'])
@login_required
def like_qaa_post(id, liked):
    data = {
        'result': 'success',
        'cancel': 'False',
        'double': 'False'
    }
    session = db_session.create_session()
    like_obj = get_LikeObj(id, 'QAA')
    if not like_obj:
        like_obj = LikeObj()
        like_obj.obj_id = id
        like_obj.type_id = get_TypeObj_id('QAA')
        session.add(like_obj)
    like = session.query(Like).filter(Like.author == current_user.id).filter(
        Like.obj_id == like_obj.id).first()
    if like:
        data['cancel'] = 'True'
        if like.dislike != liked:
            session.delete(like)
        else:
            like.dislike = not like.dislike
            data['double'] = 'True'
    else:
        like = Like()
        like.author = current_user.id
        like.obj_id = like_obj.id
        like.dislike = not liked
        like.datetime = datetime.datetime.now()
        session.add(like)
    session.commit()
    data['rating'] = get_QaaPost_rating(id)
    if data['cancel'] != 'False':
        if data['double'] != 'False':
            notification = session.query(Notification).filter(
                Notification.author == current_user.id).filter(
                Notification.to_user == session.query(QAA).get(like_obj.obj_id).author).filter(
                Notification.link_to_watch == f'/q&a/{like_obj.obj_id}').filter(
                Notification.type == get_Notification_type_id('qaa_rated')).first()
            notification.text =  f'{"decreased" if like.dislike else "raised"} the rating of your post'
            session.commit()
        else:
            notification = session.query(Notification).filter(
                Notification.author == current_user.id).filter(
                Notification.to_user == session.query(QAA).get(like_obj.obj_id).author).filter(
                Notification.link_to_watch == f'/q&a/{like_obj.obj_id}').filter(
                Notification.type == get_Notification_type_id('qaa_rated')).first()
            session.delete(notification)
            session.commit()
    else:
        if data['double'] == 'False':
            create_notification(current_user.id,
                                session.query(QAA).get(like_obj.obj_id).author,
                                f'{"decreased" if like.dislike else "raised"} the rating of your post',
                                f'/q&a/{like_obj.obj_id}', 'qaa_rated')
    return flask.jsonify(**data)


@blueprint.route('/like/qaa_comment/<int:id>/<int:liked>', methods=['GET'])
@login_required
def like_answer(id, liked):
    data = {
        'result': 'success',
        'cancel': 'False',
        'double': 'False'
    }
    session = db_session.create_session()
    like_obj = get_LikeObj(id, 'Answer')
    if not like_obj:
        like_obj = LikeObj()
        like_obj.obj_id = id
        like_obj.type_id = get_TypeObj_id('Answer')
        session.add(like_obj)
    like = session.query(Like).filter(Like.author == current_user.id).filter(
        Like.obj_id == like_obj.id).first()
    if like:
        data['cancel'] = 'True'
        if like.dislike != liked:
            session.delete(like)
        else:
            like.dislike = not like.dislike
            data['double'] = 'True'
    else:
        like = Like()
        like.author = current_user.id
        like.obj_id = like_obj.id
        like.dislike = not liked
        like.datetime = datetime.datetime.now()
        session.add(like)
    session.commit()
    data['rating'] = get_Answer_rating(id)
    if data['cancel'] != 'False':
        if data['double'] != 'False':
            notification = session.query(Notification).filter(
                Notification.author == current_user.id).filter(
                Notification.to_user == session.query(QAA).get(like_obj.obj_id).author).filter(
                Notification.link_to_watch == f'/q&a/{like_obj.obj_id}').filter(
                Notification.type == get_Notification_type_id('qaa_answer_rated')).first()
            notification.text =  f'{"decreased" if like.dislike else "raised"} the rating of your answer'
            session.commit()
        else:
            notification = session.query(Notification).filter(
                Notification.author == current_user.id).filter(
                Notification.to_user == session.query(QAA).get(like_obj.obj_id).author).filter(
                Notification.link_to_watch == f'/q&a/{like_obj.obj_id}').filter(
                Notification.type == get_Notification_type_id('qaa_answer_rated')).first()
            session.delete(notification)
            session.commit()
    else:
        if data['double'] == 'False':
            create_notification(current_user.id,
                                session.query(QAA).get(like_obj.obj_id).author,
                                f'{"decreased" if like.dislike else "raised"} the rating of your answer',
                                f'/q&a/{like_obj.obj_id}', 'qaa_answer_rated')
    return flask.jsonify(**data)


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
            form = QaaCommentForm()
            submit_data = {
                'class': 'qaa-comment-btn',
                'onclick': f'replaceQaaCommentText({str(answer.id)})'
            }
            session = db_session.create_session()
            question = session.query(QAA).get(id)
            create_notification(current_user.id,
                                question.author,
                                f'{get_user_name(current_user.id)} answered on your question: {question.title}',
                                f'/q&a/{id}', 'answered')
            return flask.jsonify({
                'result': 'success',
                'id': answer.id,
                'right_answer': answer.right_answer,
                'author': answer.author,
                'q_id': answer.qaa_id,
                'name': session.query(User).get(answer.author).name,
                'rating': get_Answer_rating(answer.id),
                'text': answer.text,
                'author_of_qaa': qaa.author == current_user.id and not session.query(Answer).filter(
                    Answer.qaa_id == qaa.id).filter(Answer.right_answer == True).first(),
                'form_hidden_tag': form.hidden_tag(),
                'form_text': form.text(id='qaa-answer-comments-hidden-input-' + str(answer.id), style='display: none'),
                'form_submit': form.submit(**submit_data)
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
            answer = session.query(Answer).get(id)
            question = session.query(QAA).get(answer.qaa_id)
            create_notification(current_user.id,
                                answer.author,
                                f'{get_user_name(current_user.id)} comment your answer on: "{question.title}"',
                                f'/q&a/{id}', 'answered')
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
    if answer.right_answer:
        create_notification(current_user.id,
                            answer.author,
                            f'{get_user_name(current_user.id)} mark your answer as right',
                            f'/q&a/{question_id}', 'mark_as_right')
    else:
        notification = session.query(Notification).filter(
            Notification.author == current_user.id).filter(
            Notification.to_user == answer.author).filter(
            Notification.link_to_watch == f'/q&a/{question_id}').filter(
            Notification.type == get_Notification_type_id('mark_as_right')).first()
        if notification:
            session.delete(notification)
            session.commit()
    return flask.jsonify({'result': 'success', 'canceled': f'{already}'})


@blueprint.route('/delete/qaa/<int:id>', methods=['GET', 'DELETE'])
@login_required
def delete_qaa(id):
    session = db_session.create_session()
    qaa = session.query(QAA).get(id)
    if current_user.id == qaa.author:
        likes = session.query(Like).filter(Like.obj_id == get_LikeObj_id(qaa.id, 'QAA')).all()
        for like in likes:
            session.delete(like)
        answers = session.query(Answer).filter(Answer.qaa_id == qaa.id).all()
        for answer in answers:
            likes = session.query(Like).filter(Like.obj_id == get_LikeObj_id(answer.id, 'Answer')).all()
            for like in likes:
                session.delete(like)
            comments = session.query(QaaComment).filter(QaaComment.answer_id == answer.id).all()
            for comment in comments:
                session.delete(comment)
            session.delete(answer)
        session.delete(qaa)
        session.commit()
    notifications = session.query(Notification).filter(Notification.link_to_watch == f'/q&a/{id}').all()
    for notification in notifications:
        session.delete(notification)
    session.commit()
    return redirect('/q&a')

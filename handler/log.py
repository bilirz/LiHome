from flask import Blueprint, render_template, session
import pymongo

bp = Blueprint('log', __name__)
mongo = pymongo.MongoClient('mongodb://127.0.0.1:27017/')


@bp.route('/log')
def log():
    if session.get('user') is None:
        session['user'] = {
            'id': -1,
            'name': 0,
            'status': 0
        }
    if session['user']['status'] == 0:
        return render_template('user/status_error.html', session=session['user'], is_index=False)
    else:
        return render_template('log.html', session=session['user'])

from flask import Blueprint, render_template, request, session
import time
import pymongo

bp = Blueprint('redblack', __name__)
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
db = client['li']
coll = db['redblack']


@bp.route('/redblack', methods=['GET', 'POST'])
def redblack():
    if session.get('user') is None:
        session['user'] = {
            'id': -1,
            'name': 0,
            'status': 0
        }
    if session['user']['status'] == 0:
        return render_template('user/status_error.html', session=session['user'], is_index=False)
    else:
        if request.method == 'POST':
            document = {'id': session['user']['id'],
                        'bid': int(request.values.get('bid')),
                        'type': int(request.values.get('type')),
                        'reason': request.values.get('reason'),
                        'time': time.time()
                        }
            coll.insert_one(document)
        return render_template('redblack/add.html', session=session['user'], users=db['user'].find())

@bp.route('/redblack/list', methods=['GET', 'POST'])
def text():
    if session.get('user') is None:
        session['user'] = {
            'id': -1,
            'name': 0,
            'status': 0
        }
    if session['user']['status'] == 0:
        return render_template('user/status_error.html', session=session['user'], is_index=False)
    else:
        return render_template('redblack/list.html', session=session['user'], redblacks=coll.find())

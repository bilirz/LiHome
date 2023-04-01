from flask import Blueprint, session, request, redirect

import pymongo

bp = Blueprint('father', __name__)
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
db = client['li']


@bp.route('/father', methods=['GET', 'POST'])
def father():
    if session.get('user') is None:
        session['user'] = {
            'id': -1,
            'name': 0,
            'status': 0
        }
    if request.method == 'POST':
        if int(request.values.get('state')) == 1:
            if session['user']['id'] != -1:
                db['user'].update_one({'id':session['user']['id']},{'$set':{'visit_all_count':db['user'].find_one({'id':session['user']['id']})['visit_all_count']+1}})
            else:
                if db['data'].find_one({'type':'visit_tourist'}) is None:
                    db['data'].insert_one({'type':'visit_tourist','count_all':0, 'count_index':0})
                else:
                    db['data'].update_one({'type':'visit_tourist'},{'$set':{'count_all':db['data'].find_one({'type':'visit_tourist'})['count_all']+1}})
    return redirect('/')

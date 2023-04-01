import time

from flask import Blueprint, render_template, session, request

import pymongo

bp = Blueprint('index', __name__)
mongo = pymongo.MongoClient('mongodb://127.0.0.1:27017/')


@bp.route('/', methods=['GET', 'POST'])
def index():
    if session.get('user') is None:
        session['user'] = {
            'id': -1,
            'name': 0,
            'status': 0
        }
    if request.method == 'POST':
        if int(request.values.get('state')) == 0:
            if session['user']['id'] != -1:
                mongo['li']['user'].update_one({'id':session['user']['id']},{'$set':{'visit_index_count':mongo['li']['user'].find_one({'id':session['user']['id']})['visit_index_count']+1}})
            else:
                mongo['li']['data'].update_one({'type':'visit_tourist'},{'$set':{'count_index':mongo['li']['data'].find_one({'type':'visit_tourist'})['count_index']+1}})
    if session['user']['status'] == 0:
        return render_template('user/status_error.html', session=session['user'], is_index=True)
    else:
        visit_all_count = 0
        visit_index_count = 0
        for user in mongo['li']['user'].find(): #all_count
            visit_all_count += user['visit_all_count']
        visit_tourist_all = mongo['li']['data'].find_one({'type':'visit_tourist'})['count_all']
        visit_all = visit_all_count + visit_tourist_all
        for user in mongo['li']['user'].find(): #index_count
            visit_index_count += user['visit_index_count']
        visit_tourist_index = mongo['li']['data'].find_one({'type':'visit_tourist'})['count_index']
        visit_index = visit_index_count + visit_tourist_index
        return render_template('index.html',
                               session=session['user'],
                               time=time.time(),
                               users_all=mongo['li']['user'].find(),
                               users_index=mongo['li']['user'].find(),
                               visit_all=visit_all,
                               visit_tourist_all=visit_tourist_all,
                               visit_index=visit_index,
                               visit_tourist_index=visit_tourist_index)

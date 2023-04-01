import hashlib, time
import pymongo

from flask import Blueprint, render_template, request, session, redirect

bp = Blueprint('user', __name__)
mongo = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
db = mongo['li']['user']


def md5(require, salt):
    md = hashlib.md5()
    md.update(str(require).encode('utf-8'))
    md.update(str(salt).encode('utf-8'))
    return md.hexdigest()


@bp.route('/user/login', methods=['GET', 'POST'])
def login():
    if session.get('user') is None:
        session['user'] = {
            'id': -1,
            'name': 0,
            'status': 0
        }
    if request.method == 'POST':
        if db.find_one({'name':request.values.get('name')}) is not None:
            if md5(request.values.get('password'), db.find_one({'name':request.values.get('name')})['time']) == db.find_one({'name':request.values.get('name')})['password']:
                session['user'] = {
                    'id':db.find_one({'name':request.values.get('name')})['id'],
                    'name':db.find_one({'name':request.values.get('name')})['name'],
                    'status': db.find_one({'name':request.values.get('name')})['status']
                    }
    return render_template('user/login.html', session=session['user'])


@bp.route('/user/register', methods=['GET', 'POST'])
def register():
    if session.get('user') is None:
        session['user'] = {
            'id': -1,
            'name': 0,
            'status': 0
        }
    if request.method == 'POST':
        time_then = time.time()
        if db.find_one() is None:
            id_ = 1
        else:
            id_ = db.find_one(sort=[( '_id', -1)])['id']+1
        document = {
            'id': id_,
            'name': request.values.get('name'),
            'password': md5(request.values.get('password'), time_then),
            'status': 1,
            'visit': 0,
            'time': time_then,
            }
        db.insert_one(document)
    return render_template('user/register.html', session=session['user'])


@bp.route('/user/out', methods=['GET', 'POST'])
def out():
    session['user'] = {
        'id': -1,
        'name': 0,
        'status': 0
    }
    return redirect('/user/login')

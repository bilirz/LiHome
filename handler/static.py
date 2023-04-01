from flask import Blueprint

bp = Blueprint('static', __name__, static_folder='./../static')


@bp.route('/favicon.ico')
def favicon():
    return bp.send_static_file('images/favicon.ico')


@bp.route('/robots.txt')
def robots():
    return bp.send_static_file('robots.txt')

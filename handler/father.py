from flask import Blueprint, render_template

bp = Blueprint('father', __name__)


@bp.route('/father')
def father():
    return render_template('father.html')

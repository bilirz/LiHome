# import logging
import time
import pymongo

from flask import Flask, render_template, session
from handler import static, father, index, log, user, redblack
import config

mongo = pymongo.MongoClient('mongodb://127.0.0.1:27017/')

app = Flask(__name__)

app.register_blueprint(static.bp)
app.register_blueprint(father.bp)
app.register_blueprint(index.bp)
app.register_blueprint(log.bp)
app.register_blueprint(user.bp)
app.register_blueprint(redblack.bp)

app.config.from_object(config)

# logging.basicConfig(level=logging.DEBUG, filename="./app.log")


@app.errorhandler(404)
def miss(error):
    return render_template('404.html', session=session['user']), 404

@app.template_filter('id_name')
def id_name(id):
    return mongo['li']['user'].find_one({'id':id})['name']

@app.template_filter('custom_time')
def custom_time(timestamp):
    time_local = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_local)

if __name__ == '__main__':
    app.run()

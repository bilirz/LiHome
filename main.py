# import logging

from flask import Flask, render_template
from handler import father, static, index
import config


app = Flask(__name__)

app.register_blueprint(father.bp)
app.register_blueprint(static.bp)
app.register_blueprint(index.bp)

app.config.from_object(config)


# logging.basicConfig(level=logging.DEBUG, filename="./app.log")


@app.errorhandler(404)
def miss(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()

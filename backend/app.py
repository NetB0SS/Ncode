from flask import Flask
from backend.apps import register_views
from backend.model.db import db


flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://spsp-server:spsp1505@10.0.6.17:3306/test'
flask_app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = flask_app
db.init_app(flask_app)



def init_app(app):
    register_views(app)

init_app(flask_app)

if __name__ == '__main__':
    flask_app.run()
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from users.users import users
from orders.orders import orders
from offers.offers import offers

import model.model
from utils import utils
import os
from model.model import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./static/database/database.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db.init_app(app)

app.register_blueprint(users)
app.register_blueprint(orders)
app.register_blueprint(offers)

with app.app_context():
    #db.drop_all()
    db.create_all()

    FOLDER_PATH = 'C:/Users/puzyn/PycharmProjects/SkyPro/homework16/static/json_datafiles/'
    for filename in os.listdir(FOLDER_PATH):
        filepath = os.path.join(FOLDER_PATH, filename)
        if 'user' in filename:
            users = utils.get_entities(filepath)
        if 'order' in filename:
            orders = utils.get_entities(filepath)
        if 'offer' in filename:
            offers = utils.get_entities(filepath)

    db.session.add_all(users)
    db.session.commit()
    db.session.add_all(offers)
    db.session.commit()
    db.session.add_all(orders)

    db.session.commit()


if __name__ == '__main__':
    app.run()
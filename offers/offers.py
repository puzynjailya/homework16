from flask import Blueprint, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from model.model import Offer
from utils.utils import instance_to_dict

offers = Blueprint('offers', __name__, url_prefix='/offers/')

db = SQLAlchemy()

offers_reference = {'order_id', 'executor_id'}


@offers.route('/', methods=['GET', 'POST'])
def orders_index_page():

    if request.method == 'GET':
        result = []
        offers = db.session.query(Offer).all()

        for offer in offers:
            result.append(instance_to_dict(offer, 'Offer'))
        return jsonify(result)

    # Если POST запрос, то
    if request.method == 'POST':
        # Получаем данные
        data = request.json

        # Не уверен, что эта проверка нужна
        # Но проверяем, что файл для запроса содержит нужные ключи
        if set(data.keys()) == offers_reference:
            # Раскрываем данные словаря и добавляем в БД
            offer = Offer(**data)
            db.session.add(offer)
            db.session.commit()
            return jsonify(data)

        else:
            return jsonify('Введены не все необходимые данные')


@offers.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def order_by_id_page(id):
    # Метод GET
    if request.method == 'GET':
        offer = db.session.query(Offer).filter(Offer.id == id).first()

        if offer is None:
            abort(404)

        return jsonify(instance_to_dict(offer, 'Offer'))

    # Метод PUT
    if request.method == 'PUT':
        # Получаем данные из запроса:
        data = request.json

        # Получаем необходимые данные пользователя по его id
        offer = db.session.query(Offer).filter(Offer.id == id).first()

        if offer is None:
            abort(404)

        db.session.query(Offer).filter(Offer.id == id).update(data)
        db.session.add(offer)
        db.session.commit()

        return jsonify(data)

    # Метод DELETE
    if request.method == 'DELETE':
        # Получаем необходимые данные пользователя по его id

        offer = db.session.query(Offer).filter(Offer.id == id).delete()

        if offer == 0:
            print('Оффер не найден')
            abort(404)

        db.session.commit()

        return jsonify(f'Оффрер с {id} удален')




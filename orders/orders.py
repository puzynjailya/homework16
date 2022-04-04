from flask import Blueprint, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from model.model import Order
from utils.utils import instance_to_dict, date_to_pythondate

orders = Blueprint('orders', __name__, url_prefix='/orders')

db = SQLAlchemy()

orders_reference = {'name', 'description', 'start_date', 'end_date',
                    'address', 'price', 'customer_id', 'executor_id'}


@orders.route('/', methods=['GET', 'POST'])
def orders_index_page():

    if request.method == 'GET':
        result = []
        orders = db.session.query(Order).all()
        for order in orders:
            result.append(instance_to_dict(order, 'Order'))
        return jsonify(result)

    # Если POST запрос, то
    if request.method == 'POST':
        # Получаем данные
        data = request.json

        # Не уверен, что эта проверка нужна
        # Но проверяем, что файл для запроса содержит нужные ключи

        if set(data.keys()) == orders_reference:
            data['start_date'] = date_to_pythondate(data['start_date'])
            data['end_date'] = date_to_pythondate(data['end_date'])
            # Раскрываем данные словаря и добавляем в БД
            order = Order(**data)
            db.session.add(order)
            db.session.commit()
            return jsonify(data)

        else:
            return jsonify('Введены не все необходимые данные')


@orders.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def order_by_id_page(id):
    # Метод GET
    if request.method == 'GET':
        order = db.session.query(Order).filter(Order.id == id).first()

        if order is None:
            abort(404)

        return jsonify(instance_to_dict(order, 'Order'))

    # Метод PUT
    if request.method == 'PUT':
        # Получаем данные из запроса:
        data = request.json

        # Проверяем на наличие дат в запросе
        if 'start_date' in data.keys():
            data['start_date'] = date_to_pythondate(data['start_date'])
        if 'end_date' in data.keys():
            data['end_date'] = date_to_pythondate(data['end_date'])

        # Получаем необходимые данные пользователя по его id
        order = db.session.query(Order).filter(Order.id == id).first()

        if order is None:
            abort(404)

        db.session.query(Order).filter(Order.id == id).update(data)
        db.session.add(order)
        db.session.commit()

        return jsonify(data)

    # Метод DELETE
    if request.method == 'DELETE':
        # Получаем необходимые данные пользователя по его id

        order = db.session.query(Order).filter(Order.id == id).delete()

        if order == 0:
            print('Заказ не найден')
            abort(404)

        db.session.commit()

        return jsonify(f'Заказ с {id} удален')




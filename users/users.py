from flask import Blueprint, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from model.model import User
from utils.utils import instance_to_dict

users = Blueprint('users', __name__, url_prefix='/users')

db = SQLAlchemy()

users_reference = {"first_name", "last_name", "age", "email", "role", "phone"}


@users.route('/', methods=['GET', 'POST'])
def users_index_page():

    if request.method == 'GET':
        result = []
        users = db.session.query(User).all()
        for user in users:
            result.append(instance_to_dict(user, 'User'))
        return jsonify(result)

    # Если POST запрос, то
    if request.method == 'POST':
        # Получаем данные
        data = request.json

        # Не уверен, что эта проверка нужна
        # Но проверяем, что файл для запроса содержит нужные ключи
        if set(data.keys()) == users_reference:

            # Раскрываем данные словаря и добавляем в БД
            user = User(**data)
            db.session.add(user)
            db.session.commit()
            return jsonify(data)

        else:
            return jsonify('Введены не все необходимые данные')


@users.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def user_by_id_page(id):
    # Метод GET
    if request.method == 'GET':
        user = db.session.query(User).filter(User.id == id).first()

        if user is None:
            abort(404)

        return jsonify(instance_to_dict(user, 'User'))

    # Метод PUT
    if request.method == 'PUT':
        # Получаем данные из запроса:
        data = request.json
        # Получаем необходимые данные пользователя по его id
        user = db.session.query(User).filter(User.id == id).first()

        if user is None:
            abort(404)
        '''
        for key in data.keys():
            if key in instance_to_dict(user, 'User').keys():
                user.key = data[key]
        '''
        db.session.query(User).filter(User.id == id).update(data)
        db.session.add(user)
        db.session.commit()

        return jsonify(data)

    # Метод DELETE
    if request.method == 'DELETE':

        # Получаем необходимые данные пользователя по его id
        user = db.session.query(User).filter(User.id == id).delete()

        if user == 0:
            print('Пользователь не найден')
            abort(404)

        db.session.commit()

        return jsonify(f'Пользователь с {id} удален')
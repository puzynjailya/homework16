import json
from model.model import *
from datetime import datetime


def date_to_pythondate(row_value):
    """
    Функция перевода даты к объектам python
    :param row_value: строка, которую необходимо заменить
    :return: объект python, приведенный к iso формату
    """
    return datetime.strptime(row_value, '%m/%d/%Y').date()


def get_entities(filepath):
    """
    Функция предназначена для раскрытия файла json и подготовки его к миграции данных
    :param filepath: Путь к файлу json
    :return: migration_list: list - список экземпляров класса, готовых к миграции данных
    """
    try:
        with open(file=filepath, mode='r', encoding='utf-8[') as file:
            data = json.load(file)
    except json.JSONDecoder as e:
        print('А файлик-то не json')
        print(e)
    except FileNotFoundError as e:
        print(f'Файл не найден по заданному пути {filepath}')
        print(e)

    # Создаем пустой список
    migration_list = []
    # Записываем данные:
    if 'users.json' in filepath:
        for row in data:
            migration_list.append(User(id=row['id'],
                                       first_name=row['first_name'],
                                       last_name=row['last_name'],
                                       age=row['age'],
                                       email=row['email'],
                                       role=row['role'],
                                       phone=row['phone']))
        return migration_list

    elif 'orders.json' in filepath:
        for row in data:
            row['start_date'] = date_to_pythondate(row['start_date'])
            row['end_date'] = date_to_pythondate(row['end_date'])

            migration_list.append(Order(id=row['id'],
                                        name=row['name'],
                                        description=row['description'],
                                        start_date=row['start_date'],
                                        end_date=row['end_date'],
                                        address=row['address'],
                                        price=row['price'],
                                        customer_id=row['customer_id'],
                                        executor_id=row['executor_id']))
        return migration_list

    elif 'offers.json' in filepath:
        for row in data:
            migration_list.append(Offer(id=row['id'],
                                        order_id=row['order_id'],
                                        executor_id=row['executor_id']))
        return migration_list


def instance_to_dict(instance, model_name):
    """
    Функция перевода объекта запроса в словарь
    :param instance: результат запроса
    :param model_name: тип модели, к которой приводим данные
    :return: словарь с даными
    """
    if model_name == 'User':
        return {'id': instance.id,
                'first_name': instance.first_name,
                'last_name': instance.last_name,
                'age': instance.age,
                'email': instance.email,
                'role': instance.role,
                'phone': instance.phone}

    if model_name == 'Offer':
        return {'id': instance.id,
                'order_id': instance.order_id,
                'executor_id': instance.executor_id}

    if model_name == 'Order':
        return{'id': instance.id,
               'name': instance.name,
               'description': instance.description,
               'start_date': instance.start_date,
               'end_date': instance.end_date,
               'address': instance.address,
               'price': instance.price,
               'customer_id': instance.customer_id,
               'executor_id': instance.executor_id}

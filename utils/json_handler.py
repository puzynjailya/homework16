import json
import os


def json_handler(filename, FOLDER_PATH):
    """
    Функция предназначена для преобразования не совсем корректных файлов json в корректные
    :param filename: путь к файлу
    :param FOLDER_PATH: путь к папке
    :return: ничего, просто преобразовывает и пересохраняет файлы
    """
    file_path = os.path.join(FOLDER_PATH, filename)

    # Если удачно, то ок
    try:
        with open(file=file_path, mode='r', encoding='cp1251') as file:
            file_data = json.load(file)
            print(f'Файл {filename} просто замечательный и я не буду ничего с ним делать')

    # Если не вышло открыть
    except json.decoder.JSONDecodeError:
        with open(file=file_path, mode='r', encoding='cp1251') as file:
            data = file.readline()
            # Заменяем символы
            data = data.replace('\'', '\"')
        with open(file=file_path, mode='w', encoding='cp1251') as file:
            json.dump(data, file, ensure_ascii=False)

    except json.JSONDecoder as e:
        print(filename)
        print(e)
    except FileNotFoundError as e:
        print(filename)
        print(e)


if __name__ == '__main__':

    FOLDER_PATH = 'C:/Users/puzyn/PycharmProjects/SkyPro/homework16/static/json_datafiles/'
    for filename in os.listdir(FOLDER_PATH):
        json_handler(filename, FOLDER_PATH)

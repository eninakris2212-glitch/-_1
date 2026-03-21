import json

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email, password):

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_api_key(self, email, password):
        """Получение ключа авторизации"""
        headers = {'email': email, 'password': password}
        res = requests.get(self.base_url+'api/key', headers=headers)
        if res.status_code == 200:
            # Сохраняем ключ авторизации в атрибут класса
            self.api_key = res.json()['key']
        return res.status_code, res.json()

    def get_api_key(self, email: str, password: str) -> tuple:

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + "/api/key", headers=headers)

        # Проверяем статус ответа
        if res.status_code == 200:
            # Если всё хорошо, возвращаем JSON-ответ
            return res.status_code, res.json()
        elif res.status_code == 403:
            # Если ошибка 403, возвращаем пустой словарь и статус
            return res.status_code, {}  # Или любое подходящее значение
        else:
            # Любая другая ошибка
            raise Exception(f"Ошибка авторизации: {res.status_code}, {res.text}")

    def update_pet_info(self, auth_key, pet_id, name, animal_type, age):
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet_simple(self, auth_key: str, name: str, animal_type: str, age: str) -> tuple:
        """ Добавляет нового питомца без фотографии.   """
        # Формирование заголовков и данных
        headers = {'auth_key': auth_key}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        # Отправка POST-запроса
        res = requests.post(self.base_url + "/api/create_pet_simple", headers=headers, data=data)

        if res.status_code == 200:
            # Успех: питомец удалён
            return res.status_code, res.json()
        elif res.status_code == 404:
            # Питомец не найден
            return res.status_code, {}
        elif res.status_code == 500:
            # Внутренняя ошибка сервера
            return res.status_code, {"error": res.text}
        else:
            # Любая другая ошибка
            raise Exception(f"Ошибка удаления питомца: {res.status_code}, {res.text}")

    def add_pet_photo(self, auth_key: str, pet_id: str, pet_photo: str):
        """ Добавляет или обновляет фотографию у существующего питомца.  """
        headers = {'auth_key': auth_key}

        try:
            with open(pet_photo, 'rb') as file:
                res = requests.post(
                    self.base_url + f'/api/pets/set_photo/{pet_id}',
                    headers=headers,
                    files={'pet_photo': file}
                )
        except FileNotFoundError:
            return 500, {"error": "Файл изображения не найден"}

        if res.status_code == 200:
            # Успех: питомец удалён
            return res.status_code, res.json()
        elif res.status_code == 404:
            # Питомец не найден
            return res.status_code, {}
        elif res.status_code == 500:
            # Внутренняя ошибка сервера
            return res.status_code, {"error": res.text}
        else:
            # Любая другая ошибка
            raise Exception(f"Ошибка удаления питомца: {res.status_code}, {res.text}")

    def get_pet_info(self, auth_key: str, pet_id: str) -> tuple:
        """ Метод для получения информации о питомце по его ID. """
        headers = {'auth_key': auth_key}

        res = requests.get(self.base_url + f'api/pets/{pet_id}', headers=headers)

        if res.status_code == 200:
            # Успех: питомец удалён
            return res.status_code, res.json()
        elif res.status_code == 404:
            # Питомец не найден
            return res.status_code, {}
        elif res.status_code == 500:
            # Внутренняя ошибка сервера
            return res.status_code, {"error": res.text}
        else:
            # Любая другая ошибка
            raise Exception(f"Ошибка удаления питомца: {res.status_code}, {res.text}")

    def delete_pet(self, auth_key, pet_id):
        """ Метод для удаления питомца по его ID. """
        headers = {'auth_key': auth_key}

        res = requests.delete(self.base_url + f'api/pets/{pet_id}', headers=headers)

        if res.status_code == 200:
            # Успех: питомец удалён
            return res.status_code, res.json()
        elif res.status_code == 404:
            # Питомец не найден
            return res.status_code, {}
        elif res.status_code == 500:
            # Внутренняя ошибка сервера
            return res.status_code, {"error": res.text}
        else:
            # Любая другая ошибка
            raise Exception(f"Ошибка удаления питомца: {res.status_code}, {res.text}")


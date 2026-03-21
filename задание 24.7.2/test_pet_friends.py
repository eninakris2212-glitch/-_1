from api import PetFriends
from settings import valid_email, valid_password
import os
import pytest
pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_update_pet_info_successfully(name="Персик", animal_type="кот", age="2"):
    '''Тест:Обновление данных о питомце по его ID.'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_get_api_key_invalid_password():
    """Тест: Авторизация с валидным email, но неверным паролем."""
    status, result = pf.get_api_key(valid_email, "wrong_password_123")
    assert status == 403, f"Ожидался статус 403 (Forbidden), получен {status}"
    assert "key" not in result, "Ключ доступа не должен быть возвращен при ошибке авторизации"

def test_get_api_key_nonexistent_email():
    """Тест: Авторизация с несуществующим email."""
    status, result = pf.get_api_key("nonexistent@mail.ru", valid_password)
    assert status == 403, f"Ожидался статус 403 (Forbidden), получен {status}"

def test_get_list_of_pets_invalid_auth_key():
    """Тест: Попытка получить список питомцев с поддельным ключом."""
    invalid_key = {"key": "invalid_fake_key_1245"}
    status, result = pf.get_list_of_pets(invalid_key, "")
    assert status == 403, f"Ожидался статус 403 (Forbidden), получен {status}"


def test_add_new_pet_simple(name="Персик", animal_type="кот", age="2"):
    '''Тест: Проверка метода простого добавления питомца без фото'''
    status, auth_key_dict = pf.get_api_key(valid_email, valid_password)
    auth_key_str = auth_key_dict['key']

    # Добавление питомца
    status, result = pf.add_new_pet_simple(auth_key_str, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_add_photo_to_nonexistent_pet():
    """Тест: Попытка добавить фото питомцу с несуществующим ID."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Используем заведомо неверный ID
    invalid_pet_id = "0"
    status, result = pf.add_pet_photo(auth_key['key'], invalid_pet_id, "imeges/cat.jpg")

    assert status == 404 or status == 403 or status == 500


def test_cannot_add_pet_with_age_more_than_three_digits():
    """
    Тест: Невозможность добавления питомца с возрастом более двух цифр.
    Ожидается, что сервер отклонит запрос с ошибкой, если возраст превышает 2 цифры.
    """
    _, auth_key_dict = pf.get_api_key(valid_email, valid_password)
    auth_key_str = auth_key_dict['key']

    # Попытка добавить питомца с возрастом более 2 цифр
    name = 'Персик'
    animal_type = 'cat'
    age = 123

    # Добавление питомца
    status, result = pf.add_new_pet_simple(auth_key_str, name, animal_type, age)

    # Проверка статуса ответа
    assert status == 400, f"Ошибка: ожидался статус 400, получен {status}"

    # Дополнительно можно проверить, что в ответе нет данных питомца
    if status != 200:
        print("Внимание: сервер принял питомца с возрастом более 2 цифр. Это баг на стороне API.")
        assert False, "Ошибка: сервер принял питомца с возрастом более 2 цифр."
    else:
        assert status in [400, 403], f"Ошибка: ожидались статусы 400 или 403, получен {status}"


def test_add_new_pet_with_negative_age():
    ''' Тест: Попытка добавить питомца с отрицательным значением возраста.'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Попытка добавить питомца с отрицательным возрастом
    status, result = pf.add_new_pet_simple(auth_key['key'], "Персик", "Кот", "-5")

    # Проверка статуса ответа
    # Ожидаем ошибку (400 или 403), но временно принимаем 200 как баг
    if status == 200:
        print("Внимание: сервер принял питомца с отрицательным возрастом (-5). Это баг на стороне API.")
        assert False, "Ошибка: сервер принял питомца с отрицательным возрастом."
    else:
        assert status in [400, 403], f"Ошибка: ожидались статусы 400 или 403, получен {status}"


def test_add_new_pet_with_empty_name():
    """Тест: Попытка добавить питомца с пустым полем 'name'."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key['key'], "", "Кот", "2")
    # API может вернуть 400 (Bad Request) или 403. Проверим оба варианта.
    if status == 200:
        print("Внимание: сервер принял питомца с пустым именем. Это баг на стороне API.")
        assert False, "Ошибка: сервер принял питомца с пустым именем. Это баг!"
    else:
        assert status in [400, 403], f"Ошибка: ожидались статусы 400 или 403, получен {status}"
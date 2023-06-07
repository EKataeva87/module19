from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

"""Тест №1"""
def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    """ Проверяем что запрос api ключа с несуществующим email возвращает статус код 403"""

    status, result = pf.get_api_key(email, password)
    assert status == 403

"""Тест №2"""
def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    """ Проверяем что запрос api ключа с несуществующим паролем возвращает статус код 403"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


"""Тест №3"""
def test_get_all_pets_with_invalid_auth_key(filter='my_pets'):
    """ Проверяем что запрос питомцев с фильтром my_pets с несуществующим api ключом возвращает статус код 403 """
    # Вводим несуществующий api ключ и отправляем запрос
    auth_key = {"key":"27fff5d09616dccba7d342e65222213cfb2b864030cd717e162b7b63"}
    status, result = pf.get_list_of_pets(auth_key, filter)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


"""Тест №4"""
def test_get_all_pets_with_filter_my_pets(filter=''):
    """  Проверяем что запрос питомцев с фильтром my_pets возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
        запрашиваем список питомцев данного пользователя и проверяем что список не пустой. """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

"""Тест №5"""

def test_add_photo_of_pet_with_invalid_pet_id():
    """Проверяем что нельзя добавить фото к несуществующему питомцу"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Вводим несуществующий ID питомца и выполняем запрос
    pet_id = "5ff5fbe9-ac74-492d-8f79-5133348495c4"
    status, result = pf.add_photo_of_pet(auth_key, pet_id, "images/cat1.jpg")

    # Проверяем что статус код ответа = 500
    assert status == 500


"""Тест №6"""
def test_add_photo_as_text_file():
    """Проверяем что нельзя добавить фото к несуществующему питомцу txt файлом"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], "images/Filename.txt")

        # Проверяем что статус код ответа = 500
        assert status == 500

    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

"""Тест №7"""
def test_get_all_pets_with_filter_integer(filter=35):
    """ Проверяем что запрос питомцев с некорректным фильтром в виде числа возвращает статус код 500 """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 500

"""Тест №8"""
def test_update_pet_info_with_invalid_pet_id(name="Rex", animal_type='dog', age=3):
    """Проверяем что нельзя внести изменения данных к несуществующему питомцу"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Вводим несуществующий ID питомца и выполняем запрос
    pet_id = "5ff5fbe9-ac74-492d-8f79-5133348495c4"
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

    # Проверяем что статус код ответа = 400
    assert status == 400

"""Тест №9"""
def test_update_pet_info_with_invalid_api_key(name="Rex", animal_type='dog', age=3):
    """Проверяем что нельзя внести изменения данных с существующим ID при введении несуществующего api ключа"""

    # Вводим несуществующий api ключ
    auth_key = {"key": "27fff5d09616dccba7d342e65222213cfb2b864030cd717e162b7b63"}

    # Вводим существующий ID питомца и выполняем запрос
    pet_id = "6ff5fbe9-ac74-492d-8f79-5133348495c4"
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

    # Проверяем что статус код ответа = 403
    assert status == 403

"""Тест №10"""
def test_delete_pet_with_invalid_api_key():
    """Проверяем что нельзя удалить питомца с существующим ID при введении несуществующего api ключа"""

    # Вводим несуществующий api ключ
    auth_key = {"key": "27fff5d09616dccba7d342e65222213cfb2b864030cd717e162b7b63"}

    # Вводим существующий ID питомца и выполняем запрос
    pet_id = "6ff5fbe9-ac74-492d-8f79-5133348495c4"
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Проверяем что статус код ответа = 403
    assert status == 403



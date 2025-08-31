import requests
from Diplom_2.config.urls import REGISTER_USER_URL
from Diplom_2.config.constants import password, name, message_existing_user, message_required_field
import random
import string
import allure

class TestRegisterUser:
    @allure.title('Проверка регистрации пользователя с валидными данными')
    @allure.description('Отправка данных на сервер методом POST')
    def test_register_user_with_valid_data(self):
        email = ''.join(random.choices(string.ascii_lowercase, k=5)) + '@test.com'
        user_data = {
            'email': email,
            'password': password,
            'name': name
        }

        response = requests.post(REGISTER_USER_URL, json=user_data)
        
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['user']['email'] == email
        assert response.json()['user']['name'] == name

    @allure.title('Проверка невозможности регистрации двух одинаковых пользователей')
    @allure.description('Отправка набора двух одинаковых данных на сервер методом POST')    
    def test_register_existing_user(self):
        email = ''.join(random.choices(string.ascii_lowercase, k=5)) + '@test.com'
        user_data = {
            'email': email,
            'password': password,
            'name': name
        }

        requests.post(REGISTER_USER_URL, json=user_data)
        response = requests.post(REGISTER_USER_URL, json=user_data)

        assert response.status_code == 403
        assert response.json()['message'] == message_existing_user

    @allure.title('Проверка невозможности регистрации пользователя без обязательного поля')
    @allure.description('Отправка данных без обязательного поля на сервер методом POST')
    def test_register_user_without_required_field(self):
        user_data = {
            'password': password,
            'name': name
        }

        response = requests.post(REGISTER_USER_URL, json=user_data)

        assert response.status_code == 403
        assert response.json()['message'] == message_required_field
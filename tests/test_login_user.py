import requests
from Diplom_2.utils.register_user import register_new_user_and_return_user_data
from Diplom_2.config.urls import LOGIN_USER_URL
from Diplom_2.config.constants import message_invalid_login_data
import allure

class TestLoginUser:
    @allure.title('Возможность залогиниться пользователем с валидными данными')
    @allure.description('Отправка валидных данных на сервер методом POST')
    def test_login_user_with_valid_data(self):
        email, password, _ = register_new_user_and_return_user_data()

        response = requests.post(LOGIN_USER_URL, json={'email': email, 'password': password})

        assert response.status_code == 200
        assert response.json()['user']['email'] == email

    @allure.title('Невозможность залогиниться с невалидным паролем')
    @allure.description('Отправка на сервер валидного логина и невалидного пароля методом POST')
    def test_login_user_with_invalid_password(self):
        email = register_new_user_and_return_user_data()

        response = requests.post(LOGIN_USER_URL, json={'email': email, 'password': 'abc'})

        assert response.status_code == 401
        assert response.json()['message'] == message_invalid_login_data

    @allure.title('Невозможность залогиниться с невалидным логином')
    @allure.description('Отправка на сервер валидного пароля и невалидного логина методом POST')
    def test_login_user_with_invalid_email(self):
        password = register_new_user_and_return_user_data()

        response = requests.post(LOGIN_USER_URL, json={'email': 'abc', 'password': password})

        assert response.status_code == 401
        assert response.json()['message'] == message_invalid_login_data
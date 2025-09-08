import requests
from Diplom_2.utils.register_user import register_new_user_and_return_user_data
from Diplom_2.config.urls import GET_USER_INFO_URL
from Diplom_2.config.constants import message_update_authorized_user
import random
import string
import allure

class TestUpdateUser:
    @allure.title('Проверка обновления данных авторизованным пользователем')
    @allure.description('Отправка данных на сервер методом PATCH')
    def test_update_authorized_user(self):
        user_token = register_new_user_and_return_user_data()[2]
        new_email = ''.join(random.choices(string.ascii_lowercase, k=5)) + '@test.com'

        updated_user = {
            'email': new_email,
            'password': '54321',
            'name': 'updated name'
        }

        response = requests.patch(GET_USER_INFO_URL, json=updated_user, headers={'Authorization': user_token})

        assert response.status_code == 200
        assert response.json()['user']['email'] == new_email
        assert response.json()['user']['name'] == 'updated name'

    @allure.title('Проверка обновления данных неавторизованным пользователем')
    @allure.description('Отправка данных на сервер методом PATCH')
    def test_update_unauthorized_user(self):
        new_email = ''.join(random.choices(string.ascii_lowercase, k=5)) + '@test.com'

        updated_user = {
            'email': new_email,
        }

        response = requests.patch(GET_USER_INFO_URL, json=updated_user)

        assert response.status_code == 401
        assert response.json()['message'] == message_update_authorized_user

        


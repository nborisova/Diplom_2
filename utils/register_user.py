import requests
from Diplom_2.config.urls import REGISTER_USER_URL
from Diplom_2.config.constants import password, name
import random
import string
import allure

@allure.step('Регистрируем нового пользователя')
def register_new_user_and_return_user_data():
    login_pass = []

    email = ''.join(random.choices(string.ascii_lowercase, k=5)) + '@test.com'
    
    user_data = {
        'email': email,
        'password': password,
        'name': name
    }

    response = requests.post(REGISTER_USER_URL, json=user_data)

    if response.status_code == 200:
        user_token = response.json()['accessToken']
        login_pass.append(email)
        login_pass.append(password)
        login_pass.append(user_token)

    return login_pass

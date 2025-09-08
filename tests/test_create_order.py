import requests
from Diplom_2.utils.register_user import register_new_user_and_return_user_data
from Diplom_2.config.urls import GET_AND_CREATE_ORDERS_URL
from Diplom_2.config.constants import ingredients, massage_for_order_without_ingredients
import allure


class TestCreateOrder:
    @allure.title('Возможность создания заказа авторизованным пользователем')
    @allure.description('Отправка валидных данных на сервер методом POST')
    def test_create_order_by_authorized_user(self):
        email, password, user_token = register_new_user_and_return_user_data()

        response = requests.post(GET_AND_CREATE_ORDERS_URL, json=ingredients, headers={'Authorization': user_token})

        assert response.status_code == 200
        assert response.json()['order']['owner']['email'] == email
    
    @allure.title('Возможность создания заказа неавторизованным пользователем')
    @allure.description('Отправка валидных данных на сервер методом POST')
    def test_create_order_by_unauthorized_user(self):
            response = requests.post(GET_AND_CREATE_ORDERS_URL, json=ingredients)

            assert response.status_code == 200
            assert 'name' in response.json()

    @allure.title('Невозможность создания заказа без указания ингредиентов')
    @allure.description('Отправка невалидных данных на сервер методом POST')
    def test_create_order_by_unauthorized_user_without_ingredients(self):
            response = requests.post(GET_AND_CREATE_ORDERS_URL, json={'ingredients': []})

            assert response.status_code == 400
            assert response.json()['message'] == massage_for_order_without_ingredients

    @allure.title('Невозможность создания заказа с невалидным хэшем ингредиента')
    @allure.description('Отправка невалидных данных на сервер методом POST')
    def test_create_order_by_unauthorized_user_with_invalid_ingredient_hash(self):
            response = requests.post(GET_AND_CREATE_ORDERS_URL, json={'ingredients': ['123']})

            assert response.status_code == 500
      
            

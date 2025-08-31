import requests
from Diplom_2.utils.register_user import register_new_user_and_return_user_data
from Diplom_2.config.urls import GET_AND_CREATE_ORDERS_URL
from Diplom_2.config.constants import ingredients, message_for_getting_orders_of_unauthorized_user
import allure


class TestGetOrders:
    @allure.title('Получение заказов авторизованного пользователя')
    @allure.description('Запрос на сервер методом GET с передачей токена')
    def test_get_orders_of_authorized_user(self):
        _, _, user_token = register_new_user_and_return_user_data()
        requests.post(GET_AND_CREATE_ORDERS_URL, json=ingredients, headers={'Authorization': user_token})
        requests.post(GET_AND_CREATE_ORDERS_URL, json=ingredients, headers={'Authorization': user_token})

        response = requests.get(GET_AND_CREATE_ORDERS_URL, headers={'Authorization': user_token})
        list_of_orders = response.json()['orders'] 

        assert response.status_code == 200
        assert len(list_of_orders) == 2

    @allure.title('Получение заказов неавторизованного пользователя')
    @allure.description('Запрос на сервер методом GET без передачи токена')
    def test_get_orders_of_unauthorized_user(self):
        response = requests.get(GET_AND_CREATE_ORDERS_URL)

        assert response.status_code == 401
        assert response.json()['message'] == message_for_getting_orders_of_unauthorized_user
            
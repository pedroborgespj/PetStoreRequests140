# 1 - bibliotecas
import pytest    # framework de teste de unidade / engine
import requests  # framework de teste de API
import json

# 2 - clase (opcional no Python, em muitos casos)

# 2.1 - Atributos ou variaveis

# consulta e resultado esperado
order_id = 1942144002
order_pet_id = 194214401
order_quantity = 1
order_ship_date = "2024-05-26T18:32:24.567Z"
order_status = "approved"
order_complete = True

url='https://petstore.swagger.io/v2/store/order'
headers = {'Content-type': 'application/json'}

# 2.2 - funções / métodos

def test_post_order():
    order = open('./fixtures/json/order1.json')
    data = json.loads(order.read())

    response = requests.post(
        url = url,
        headers = headers,
        data = json.dumps(data),
        timeout = 5
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['petId'] == order_pet_id
    assert response_body['quantity'] == order_quantity
    assert response_body['status'] == order_status

def test_get_order():
    response = requests.get(
        url= f'{url}/{order_id}',
        headers= headers
        # nao tem corpo da mensagem / body
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == order_id
    assert response_body['status'] == order_status
    assert response_body['complete'] == order_complete

def test_delete_order():
    response = requests.delete(
        url = f'{url}/{order_id}',
        headers= headers
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == str(order_id)

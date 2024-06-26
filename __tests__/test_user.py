# 1 - bibliotecas
import pytest    # framework de teste de unidade / engine
import requests  # framework de teste de API
import json

from utils.utils import ler_csv

# 2 - clase (opcional no Python, em muitos casos)

# 2.1 - Atributos ou variaveis

# consulta e resultado esperado
user_id = 193214401
user_username = "adrianaester"
user_first_name = "Adriana"
user_last_name = "Ester"
user_email = "adriana-darocha80@i9pneus.com.br"
user_password = "f5kkSChDSQ"
user_phone = "(51)99943-3033"
user_status = 0

url='https://petstore.swagger.io/v2/user'
headers = {'Content-type': 'application/json'}

# 2.2 - funções / métodos

def test_post_user():
    user = open('./fixtures/json/user1.json')
    data = json.loads(user.read())
    # dados de saída / resultado esperado estão no atributos das funções

   
    response = requests.post(
        url = url,
        headers = headers,
        data = json.dumps(data),
        timeout = 5
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == str(user_id)

def test_get_user():
    response = requests.get(
        url= f'{url}/{user_username}',
        headers= headers
        # nao tem corpo da mensagem / body
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == user_id
    assert response_body['username'] == user_username
    assert response_body['email'] == user_email

def test_put_user():
    user = open('./fixtures/json/user2.json')
    data = json.loads(user.read())

    response = requests.put(
        url = f'{url}/{user_username}',
        headers = headers,
        data = json.dumps(data),
        timeout = 5
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == str(user_id)

def test_delete_user():
    response = requests.delete(
        url= f'{url}/{user_username}',
        headers= headers
        # nao tem corpo da mensagem / body
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == user_username

@pytest.mark.parametrize('user_id, username, first_name, last_name, user_email, user_password, user_phone, user_status',
                         ler_csv('./fixtures/csv/users.csv') 
                        )

def test_post_user_dinamico(user_id, username, first_name, last_name, user_email, user_password, user_phone, user_status):
    user = {}
    user['id'] = int(user_id)
    user['username'] = username
    user['firstName'] = first_name
    user['lastName'] = last_name
    user['email'] = user_email
    user ['password'] = user_password
    user['phone'] = user_phone
    user['userStatus'] = int(user_status)
    
    user = json.dumps(obj=user, indent=4)

    response = requests.post(
        url=url,
        headers=headers,
        data=user,
        timeout=5
    )

    response_body = response.json()

    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == user_id

@pytest.mark.parametrize('username', 
                         [row[1] for row in ler_csv('./fixtures/csv/users.csv')]
                        )

def test_delete_user_dinamico(username):
    response = requests.delete(
        url= f'{url}/{username}',
        headers= headers
        # nao tem corpo da mensagem / body
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == username

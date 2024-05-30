# 1 - bibliotecas
import pytest    # framework de teste de unidade / engine
import requests  # framework de teste de API
import json

from utils.utils import ler_csv

# 2 - clase (opcional no Python, em muitos casos)

# 2.1 - Atributos ou variaveis

# consulta e resultado esperado
pet_id = 193214401
pet_name = "Beth"
pet_category_id = 1
pet_category_name = "dog"
pet_tag_id = 1
pet_tag_name = "vacinado"

url='https://petstore.swagger.io/v2/pet'
headers = {'Content-type': 'application/json'}

# 2.2 - funções / métodos

def test_post_pet():
    # configura
    # dados de entrada estão no arquivo json
    pet = open('./fixtures/json/pet1.json')         # abre o arquivo json
    data = json.loads(pet.read())                   # ler o conteudo e carrega como json em uma variavel data
    # dados de saída / resultado esperado estão no atributos das funções

    # executa
    response = requests.post(                       # executa o metdod post com as informações a seguir
        url = url,
        headers = headers,
        data = json.dumps(data),
        timeout = 5
    )

    # valida
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == pet_id
    assert response_body['name'] == pet_name
    assert response_body['category']['name'] == pet_category_name
    assert response_body['tags'][0]['name'] == pet_tag_name

def test_get_pet():
    # Configura
    # Dados de entrada e saída / resultado esperado estão na seção de atributos antes das funções

    # Executa
    response = requests.get(
        url= f'{url}/{pet_id}',
        headers= headers
        # nao tem corpo da mensagem / body
    )

    # Valida
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['name'] == pet_name
    assert response_body['category']['id'] == pet_category_id
    assert response_body['tags'][0]['id'] == pet_tag_id
    assert response_body['status'] == 'available'

def test_put_pet():
    pet = open('./fixtures/json/pet2.json')
    data = json.loads(pet.read())

    response = requests.put(
    url = url,
    headers = headers,
    data = json.dumps(data),
    timeout = 5
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == pet_id
    assert response_body['name'] == pet_name
    assert response_body['category']['id'] == pet_category_id
    assert response_body['category']['name'] == pet_category_name
    assert response_body['tags'][0]['id'] == pet_tag_id
    assert response_body['tags'][0]['name'] == pet_tag_name
    assert response_body['status'] == 'sold'

def test_delete_pet():
    # Configura
    # Dados de entrada e saída / resultado esperado estão na seção de atributos antes das funções

        # Executa
    response = requests.delete(
        url= f'{url}/{pet_id}',
        headers= headers
        # nao tem corpo da mensagem / body
    )

    # Valida
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == str(pet_id)

@pytest.mark.parametrize('pet_id,category_id,category_name,pet_name,tags,status',
                         ler_csv('./fixtures/csv/pets.csv') 
                        )

def test_post_pet_dinamico(pet_id, category_id, category_name, pet_name, tags, status):
    pet = {}
    pet['id'] = int(pet_id)
    pet['category'] = {}
    pet['category']['id'] = int(category_id)
    pet['category']['name'] = category_name
    pet['name'] = pet_name
    pet['photoUrls'] = []
    pet['photoUrls'].append('')
    pet['tags'] = []
    
    tags = tags.split(';')
    for tag in tags:
        tag = tag.split('-')
        tag_formatada = {}
        tag_formatada['id'] = int(tag[0])
        tag_formatada['name'] = tag[1]
        pet['tags'].append(tag_formatada)
    
    pet['status'] = status

    pet = json.dumps(obj=pet, indent=4)
    # print('\n' + pet)

    response = requests.post(
        url=url,
        headers=headers,
        data=pet,
        timeout=5   
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == int(pet_id)
    assert response_body['name'] == pet_name
    assert response_body['status'] == status
# 1 - bibliotecas
import pytest    # framework de teste de unidade / engine
import requests  # framework de teste de API
import json

# 2 - clase (opcional no Python, em muitos casos)

# 2.1 - Atributos ou variaveis

# consulta e resultado esperado
pet_id = 193214401
pet_name = "Beth"
pet_category_id = 1
pet_category_name = "dog"
pet_tag_id = 1
pet_tag_name = "vacinado"
pet_status = "available"

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


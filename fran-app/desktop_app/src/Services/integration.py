# Este arquivo é responsável por enviar os dados locais ao servidor web
import time

import requests

data_endpoint = 'http://localhost:3000/postdata'

productData = {
    'product_id': 1,
    'name': 'Bolo de abacaxi',
    'description': 'Bolo de abacaxi com cobertura',
    'price': 199.99,
}

for i in range(5):
    print(f'Iniciando envio de dados para {data_endpoint}')
    r = requests.post(url=data_endpoint, data=productData)
    time.sleep(5)
    print('status da operação: ', r.status_code)
    print(f'envios restantes: {5 - i - 1}')
    time.sleep(1)


# TODO: Este arquivo deve usar a implementação 'IntegrationFacade.py' para que tenha acesso
# indireto aos controllers.

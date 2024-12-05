# Este arquivo é responsável por enviar os dados locais ao servidor web
import time
import os
from IntegrationFacade import IntegrationFacade
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import table_registry
from urllib.parse import urlencode

data_endpoint = 'http://localhost:3000/postdata'

# Configurações do banco de dados
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, '..', 'test.db')
engine = create_engine(f'sqlite:///{db_path}')
table_registry.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Instância da classe que implementa o pattern Facade
integrationFacade = IntegrationFacade(session=db)

# print(integrationFacade.list_products())
# print("pula linha")
# print(integrationFacade.list_products_in_dict())

encoded_data_products = urlencode({"products": integrationFacade.list_products()})

for i in range(5):
    print(f'Iniciando envio de dados para {data_endpoint} em formato de lista')
    r = requests.post(url=data_endpoint, data=encoded_data_products)
    time.sleep(5)
    print('status da operação: ', r.status_code)
    print(f'envios restantes: {5 - i - 1}')
    time.sleep(1)


for i in range(5):
    print(f'Iniciando envio de dados para {data_endpoint} em formato de dicionário')
    r = requests.post(url=data_endpoint, data=integrationFacade.list_products_in_dict())
    time.sleep(5)
    print('status da operação: ', r.status_code)
    print(f'envios restantes: {5 - i - 1}')
    time.sleep(1)    



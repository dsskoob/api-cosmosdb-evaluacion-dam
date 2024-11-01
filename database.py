from azure.cosmos import CosmosClient, exceptions

COSMOS_ENDPOINT = 'https://acdb-dam-evaluacion.documents.azure.com:443/'
COSMOS_KEY = '79l79tybmJNKZIDal6CxopkcJ5H36dmB7keJsBAd9EgrhrurmBizwAUh4cE5wJsDfkqFCfBWwT8GACDbKnzNDA=='

DATABASE_NAME = 'proyectos_db'
CONTAINER_NAME = 'usuario'
CONTAINER2_NAME = 'proyecto'

#Inicializa cliente de cosmos
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

# Crear o obtener la base de datos
try:
    database = client.create_database_if_not_exists(id=DATABASE_NAME)
except exceptions.CosmosResourceExistsError:
    database = client.get_database_client(DATABASE_NAME)

# Crear u obtener el contenedor
try:
    container = database.create_container_if_not_exists(
        id=CONTAINER_NAME,
        partition_key={'paths': ['/id'], 'kind': 'Hash'},
        offer_throughput=400
    )
except exceptions.CosmosResourceExistsError:
    container = database.get_container_client(CONTAINER_NAME)

try:
    container2 = database.create_container_if_not_exists(
        id=CONTAINER2_NAME,
        partition_key={'paths': ['/id'], 'kind': 'Hash'},
        offer_throughput=400
    )
except exceptions.CosmosResourceExistsError:
    container2 = database.get_container_client(CONTAINER2_NAME)
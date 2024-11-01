from azure.cosmos import CosmosClient, exceptions

COSMOS_ENDPOINT = 'https://acdb-dam-evaluacion.documents.azure.com:443/'
COSMOS_KEY = '79l79tybmJNKZIDal6CxopkcJ5H36dmB7keJsBAd9EgrhrurmBizwAUh4cE5wJsDfkqFCfBWwT8GACDbKnzNDA=='

DATABASE_NAME = 'proyectos_db'
USUARIO_CONTAINER = 'usuario'
PROYECTO_CONTAINER = 'proyecto'

#Inicializa cliente de cosmos
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

# Obtener los contenedores
usuario_container = client.get_database_client(DATABASE_NAME).get_container_client(USUARIO_CONTAINER)
proyecto_container = client.get_database_client(DATABASE_NAME).get_container_client(PROYECTO_CONTAINER)
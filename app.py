from fastapi import FastAPI, HTTPException, Query, Path
from typing import List, Optional
from database import usuario_container, proyecto_container
from models import Usuario, Proyecto
from azure.cosmos import exceptions
from datetime import datetime

app = FastAPI(title='API de Gestion de Usuarios y Proyectos')


@app.get('/')
def home():
    return "Hola Mundo"



############################# Endpoint de Usuarios #############################

@app.post('/usuarios/', response_model=Usuario, status_code=201)
def crear_usuario(usuario: Usuario):
    try:
        # insertar elemento
        usuario_container.create_item(body=usuario.dict())
        return usuario
    except exceptions.CosmosResourceExistsError:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail= str(e))


@app.get('/usuarios/{usuario_id}')
def obtener_usuario(usuario_id:str = Path(..., description="Id del usuario a obtener")):
    try:
        usuario = usuario_container.read_item(item=usuario_id, partition_key=usuario_id)
        return usuario
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail= str(e))


@app.get('/usuarios/', response_model=List[Usuario])
def obtener_lista_usuarios():
    try:
        script = 'select * from c WHERE 1 = 1'
        items = list(usuario_container.query_items(query=script,enable_cross_partition_query=True))
        return items
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="No contiene usuarios")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail= str(e))
 

@app.put('/usuarios/{usuario_id}', response_model=Usuario)
def actualiza_usuario(usuario_id:str, updated_usuario: Usuario):
    try:
        existing_usuario = usuario_container.read_item(item=usuario_id, partition_key=usuario_id)

        existing_usuario.update(updated_usuario.dict(exclude_unset=True))
        existing_usuario['id'] = usuario_id

        usuario_container.replace_item(item=usuario_id, body=existing_usuario)

        return existing_usuario
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail= str(e))
 

@app.delete('/usuarios/{usuario_id}', status_code=204)
def eliminar_usuario(usuario_id:str):
    try:
        usuario_container.delete_item(item=usuario_id, partition_key=usuario_id)
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail= str(e))
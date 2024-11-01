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



############################# Endpoint de Proyectos #############################

@app.post("/proyectos/", response_model=Proyecto, status_code=201)
def crear_proyecto(proyecto: Proyecto):

    try:
        #Obtener usuario
        proyecto_dict = proyecto.dict()
        usuario_id = proyecto_dict['id_usuario']

        try:
            usuario = usuario_container.read_item(item=usuario_id, partition_key=usuario_id)
        except exceptions.CosmosResourceNotFoundError:
            raise HTTPException(status_code=404, detail="El usuario no existe")

        # insertar proyecto
        proyecto_container.create_item(body=proyecto_dict)

        return proyecto_dict
    except exceptions.CosmosResourceExistsError:
        raise HTTPException(status_code=400, detail="El proyecto ya existe")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get('/proyectos/', response_model=List[Proyecto])
def obtener_lista_proyectos():
    try:
        script = 'select * from c WHERE 1 = 1'
        proyectos_list = list(proyecto_container.query_items(query=script,enable_cross_partition_query=True))
        return proyectos_list
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="No contiene proyectos")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail= str(e))
 

@app.get('/usuarios/{usuario_id}/proyectos/', response_model=List[Proyecto])
def obtener_lista_proyectos_usuario(usuario_id: str):
    try:
        script = f"SELECT * FROM c WHERE c.id_usuario = '{usuario_id}'"
        proyectos_list = list(proyecto_container.query_items(query=script, enable_cross_partition_query=True))

        if not proyectos_list:
            raise HTTPException(status_code=404, detail="No contiene proyectos")
        
        return proyectos_list
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="No contiene proyectos")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))

 

@app.put("/proyectos/{proyecto_id}", response_model=Proyecto)
def actualiza_proyecto(proyecto_id: str, updated_proyecto: Proyecto):
    try:
        #Obtener usuario
        updated_proyecto_dict = updated_proyecto.dict()
        usuario_id = updated_proyecto_dict['id_usuario']

        try:
            usuario = usuario_container.read_item(item=usuario_id, partition_key=usuario_id)
        except exceptions.CosmosResourceNotFoundError:
            raise HTTPException(status_code=404, detail="El usuario no existe")

        #Obtiene proyecto
        existing_proyecto = proyecto_container.read_item(item=proyecto_id, partition_key=proyecto_id)

        existing_proyecto.update(updated_proyecto.dict(exclude_unset=True))
        existing_proyecto['id'] = proyecto_id

        proyecto_container.replace_item(item=proyecto_id, body=existing_proyecto)
 
        return existing_proyecto
        
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Proyecto no encotrado')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))

 
@app.delete("/proyectos/{proyecto_id}", status_code=204)
def eliminar_proyecto(proyecto_id: str):
    try:
        proyecto_container.delete_item(item=proyecto_id, partition_key=proyecto_id)
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail= str(e))
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# * Add the prefix on APIRouter if you want have unify the prefix ej: APIRouter(prefix='/user')
# * you can have the tag, to divide in documentation the order or prefix
router = APIRouter()

class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int

users_list = [
         User(id= 1,name = "brian",surname = "salinas", age = 25 ),
         User(id= 2,name = "paul",surname = "jara", age = 22 ),
         User(id= 3,name = "dev",surname = "veloper", age = 16 )]

@router.get('/')
async def root():
    return list(users_list)

@router.get('/')
async def users():
    return list(users_list)

@router.get('/user/{id}')
async def user(id: int):
    user = filter(lambda user: user.id == id, users_list)
    
    try:
        return list(user)[0]
    except:
        return {"error": "No se encontro el usuario"}
    
@router.get('/userquery/')
async def user(id: int):
    user = filter(lambda user: user.id == id, users_list)
    
    try:
        return list(user)[0]
    except:
        return {"error": "No se encontro el usuario"}
    
    

@router.post('/create_user/', status_code = 201)
async def create_user(user: User):
    if type(search_user(user.id)) == User:
        #!Usar la linea de abajo para manejar excepciones ***⬇
        raise HTTPException(status_code = 404, detail= "El usuario ya existe")
    
    else: 
        users_list.append(user)
        return {"message": "usuario crado con exito"}
    
    
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se encontro el usuario"}
    
    
@router.put('/user/')
async def user(user: User):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            
@router.delete('/user/{id}')
async def user(id: int):
     for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            return {"message": f"se elimino correctamente el usuario con id {index + 1}"}
        
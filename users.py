from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int

users_list = [
         User(id= 1,name = "brian",surname = "salinas", age = 25 ),
         User(id= 2,name = "paul",surname = "jara", age = 22 ),
         User(id= 3,name = "dev",surname = "veloper", age = 16 )]

# @app.get('/users')
# async def users():
#     return users_list

@app.get('/user/{id}')
async def user(id: int):
    user = filter(lambda user: user.id == id, users_list)
    
    try:
        return list(user)[0]
    except:
        return {"error": "No se encontro el usuario"}
    
@app.get('/userquery/')
async def user(id: int):
    user = filter(lambda user: user.id == id, users_list)
    
    try:
        return list(user)[0]
    except:
        return {"error": "No se encontro el usuario"}
    
    
@app.post('/user/')
async def user(user: User):
    users_list.append(user)
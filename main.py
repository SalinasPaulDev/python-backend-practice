from fastapi import FastAPI
from router import users,jwt_auth


app = FastAPI()
app.include_router(users.router)
app.include_router(jwt_auth.router)

@app.get('/saludo')
async def root():
    return "hola fastApi"

@app.get('/name')
async def name():
    return {"nombre": "Brian"}
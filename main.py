from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return "hola fastApi"

@app.get('/name')
async def name():
    return {"nombre": "Brian"}
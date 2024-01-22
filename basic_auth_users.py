from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

auth_security = OAuth2PasswordBearer(tokenUrl='login')

app = FastAPI()

class User(BaseModel):
    username : str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str
    
users_db = {
    "brianpaulsj": {
        "username" : "brianpaulsj",
        "full_name": "Brian Paul",
        "email": "salinaspaul@gmail.com",
        "disabled": False,
        "password": "123456"
    },
    "brianpaulsj2": {
        "username" : "brianpaulsj2",
        "full_name": "Brian Paul 2",
        "email": "salinaspaul2@gmail.com",
        "disabled": True,
        "password": "6789"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def current_user(token: str = Depends(auth_security)):
    user = search_user(token)
    if not user:
        raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="No estas autorizado para ingresar",
                headers={"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail="El usuario esta deshabilitado")
    return user
        
    
@app.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="La contraseña es incorrecta")
    
    return {"access_token": user.username, "token_type": "bearer"}



@app.get('/users/me')
async def me(user: User = Depends(current_user)):
    return user
    
    
    
    
    
    

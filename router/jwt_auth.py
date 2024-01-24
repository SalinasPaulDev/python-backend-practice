from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

auth_security = OAuth2PasswordBearer(tokenUrl='login')
crypt = CryptContext(schemes=["bcrypt"])

router = APIRouter()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
SECRET = "D657D9EB5BDAB11C11C49EFA4CF5F"


class User(BaseModel):
    username : str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str
    
class Token(BaseModel):
    access_token:str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None



users_db = {
    "brianpaulsj": {
        "username" : "brianpaulsj",
        "full_name": "Brian Paul",
        "email": "salinaspaul@gmail.com",
        "disabled": False,
        "password": "$2a$12$ZWDWTf1aooESsXn9/yBJ0exiOUmkGOKoyFHOHuTnFbmxUPwayAFy2"
    },
    "brianpaulsj2": {
        "username" : "brianpaulsj2",
        "full_name": "Brian Paul 2",
        "email": "salinaspaul2@gmail.com",
        "disabled": True,
        "password": "$2a$12$5Zpt8QpndtkYW25h9.mv8O3VkKMLfbi0pcYMGihdCdL5vLrys8wgq"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token: str = Depends(auth_security)):
    #* Explicacion: con jwt vas a poder decodificar el token recibido, la depencia hace referencia a auth_security que esta declarado arriba. Para la decodificacion del token necesitamos los mismos valores que usamos para codificarlo ej: token, SECRET, ALGORITHM. Esto devuelve un JSON con sub = "usuario", exp = "expiracion", etc. Con el get Obtenemos el sub que hace refencia al username
    
    
    try:      
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="No estas autorizado para ingresar",
                headers={"WWW-Authenticate": "Bearer"})
         
        return search_user(username)

    except JWTError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="No estas autorizado para ingresar",
            headers={"WWW-Authenticate": "Bearer"})

    
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail="El usuario esta deshabilitado")
    return user


@router.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    
    
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="La contraseña es incorrecta")
    
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = {"sub": user.username, "exp": expire_time}
    
    #* Crear el endcode del access token con el access token creado recientemente con sub y exp, mas el algoritmo y la secret
    return {"access_token": jwt.encode(access_token,SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get('/users/me')
async def me(user: User = Depends(current_user)):
    return user
    
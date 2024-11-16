import os
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
#import jwt
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def check_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as error:
        if 'exp' in str(error):
            raise HTTPException(status_code=401, detail="Token expirado")
        raise HTTPException(status_code=401, detail="Token inválido")

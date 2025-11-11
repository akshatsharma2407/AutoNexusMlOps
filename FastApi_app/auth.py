from datetime import datetime, timedelta, timezone
from authlib.jose import JoseError, jwt
from fastapi import HTTPException
from passlib.context import CryptContext

SECRET_KEY = 'my_secret'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRY_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def create_access_token(data: dict):
    header = {'alg':ALGORITHM}
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    payload = data.copy()
    payload.update({'exp':expire})
    return jwt.encode(header, payload, SECRET_KEY).decode('utf-8')

def verify_token(token: str):
    try:
        claims = jwt.decode(token, SECRET_KEY)
        claims.validate()
        username = claims.get('sub')
        if username is None:
            raise HTTPException(status_code=401, detail='Token Missing')
        return username
    except JoseError:
        raise HTTPException(status_code=401, detail="could not validate credentials")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from FastApi_app import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def register_user(db: Session, user: schemas.User):
    hashed_password = pwd_context.hash(user.password_hash)
    db_user = models.User(first_name = user.first_name, last_name = user.last_name,email=user.email, password_hash = hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_details(db: Session, email):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user
from sqlalchemy.orm import Session
from . import models, schemas, auth


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email,
                          full_name=user.full_name,
                          hashed_password=auth.get_password_hash(user.password)
                          )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def update_user(
        db: Session, db_user: models.User, user_update: schemas.UserUpdate
):
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

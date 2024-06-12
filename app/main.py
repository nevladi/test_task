from datetime import timedelta
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app import models, schemas, crud, database, auth


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
        db: Session = Depends(database.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.User)
def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(database.get_db)
):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    return crud.create_user(db=db, user=user)


@app.get("/users/me", response_model=schemas.User)
async def read_users_me(
        current_user: schemas.User = Depends(auth.get_current_active_user)
):
    return current_user


@app.put("/users/me", response_model=schemas.User)
async def update_user_me(
    user_update: schemas.UserUpdate,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    return crud.update_user(
        db=db, db_user=current_user, user_update=user_update
    )


@app.get("/products/", response_model=List[schemas.Product])
def read_products(
        skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)
):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


@app.post("/products/", response_model=schemas.Product)
def create_product(
        product: schemas.ProductCreate, db: Session = Depends(database.get_db)
):
    return crud.create_product(db=db, product=product)


@app.post("/orders/", response_model=schemas.Order)
def create_order(
        order: schemas.OrderCreate, db: Session = Depends(database.get_db)
):
    return crud.create_order(db=db, order=order)

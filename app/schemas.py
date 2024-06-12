from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    full_name: str | None


class UserCreate(UserBase):
    username: str
    email: str
    full_name: str | None
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: str | None
    password: str | None


class ProductBase(BaseModel):
    name: str
    description: str
    price: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    user_id: int
    product_id: int


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None

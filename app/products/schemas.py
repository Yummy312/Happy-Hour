from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=3)
    description: str = Field(min_length=4)
    price: int = Field(gt=0)
    quantity: int = Field(gt=0)


class ProductCreate(ProductBase):
    company_id: int


class ProductRetrieve(ProductBase):
    id: int


class ProductDetail(ProductCreate, ProductRetrieve):
    pass

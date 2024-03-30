from pydantic import BaseModel, Field


class CompanyBase(BaseModel):
    name: str = Field(min_length=3)
    description: str = Field(min_length=5)
    location: str = Field(min_length=4)
    hours_of_operation: str


class CompanyRetrieve(CompanyBase):
    id: int

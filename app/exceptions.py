from fastapi import HTTPException, status

CompanyNotExists = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="company not found"
)
CompanyByIdNotExists = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="company with id not found"
)

CompanyExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="company already exists"
)

ProductExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="product already exists"
)
ProductNotExists = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="product not found"
)
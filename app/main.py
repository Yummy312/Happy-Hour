from fastapi import FastAPI
from app.products.router import router as products_router
from app.companies.router import router as companies_router
app = FastAPI(
    title='Happy Hour'

)
app.include_router(companies_router)
app.include_router(products_router)

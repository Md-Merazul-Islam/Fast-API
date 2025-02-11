from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .models import Product, Category
from .schemas import ProductCreate, ProductInResponse
from .crud import create_product, get_products, generate_dummy_data
from .database import get_db
# Create the database tables
from . import models, schemas, crud
from .database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# Dependency to get the DB session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/generate-dummy-products/")
async def generate_and_add_products(db: Session = Depends(get_db)):
    generate_dummy_data(db)  # Pass db to the function
    return {"message": "10,000 dummy products added successfully."}


@app.post("/products/", response_model=ProductInResponse)
async def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)  # Pass db to the function


@app.get("/products/")
async def read_products(db: Session = Depends(get_db)):
    return get_products(db)  # Pass db to the function


@app.post("/category/", response_model=schemas.CategoryView)
def create_category(category: schemas.CategoryInput, db: Session = Depends(get_db)):
    # Pass db and category to the function
    db_category = crud.create_category(db=db, category=category)
    return db_category


def get_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category(db, category_id)  # Pass db to the function
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

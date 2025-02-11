# from fastapi import FastAPI, Depends
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.future import select
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# from databases import Database

# # Database URL (replace with your actual credentials)
# DATABASE_URL = "postgresql+asyncpg://fastaoi_user:AabqU9Wfo9DiNNhcmqQDKNbo2DWHyvUL@dpg-culd85hu0jms739oi84g-a.oregon-postgres.render.com/fastaoi"

# # FastAPI application setup
# app = FastAPI()

# # SQLAlchemy Database setup (Async)
# Base = declarative_base()

# # Async engine and session maker setup
# engine = create_async_engine(DATABASE_URL, echo=True)
# async_session = sessionmaker(
#     engine, class_=AsyncSession, expire_on_commit=False
# )

# # Dependency to get the database session
# async def get_db():
#     async with async_session() as session:
#         yield session

# # Example Model
# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)

# # Initialize Database
# async def init_db():
#     async with engine.begin() as conn:
#         # Create all tables
#         await conn.run_sync(Base.metadata.create_all)

# @app.on_event("startup")
# async def on_startup():
#     # Initialize the database on startup
#     await init_db()

# # Example route
# @app.get("/users/")
# async def get_users(db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(User))
#     users = result.scalars().all()
#     return users


from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

# Database URL (replace with your actual credentials)
DATABASE_URL = "postgresql+asyncpg://fastaoi_user:AabqU9Wfo9DiNNhcmqQDKNbo2DWHyvUL@dpg-culd85hu0jms739oi84g-a.oregon-postgres.render.com/fastaoi"

# FastAPI application setup
app = FastAPI()

# SQLAlchemy Database setup (Async)
Base = declarative_base()

# Async engine and session maker setup
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency to get the database session
async def get_db():
    async with async_session() as session:
        yield session

# Product model definition
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float)

# Pydantic Product schema for input/output validation
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float

class ProductResponse(ProductCreate):
    id: int

    class Config:
        orm_mode = True

# Initialize Database
async def init_db():
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    # Initialize the database on startup
    await init_db()

# Create Product API Route
@app.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

# Get All Products API Route
@app.get("/products/", response_model=list[ProductResponse])
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return products

# Get Single Product by ID API Route
@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product = result.scalars().first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Update Product API Route
@app.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    db_product = result.scalars().first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    await db.commit()
    await db.refresh(db_product)
    return db_product

# Delete Product API Route
@app.delete("/products/{product_id}", response_model=ProductResponse)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    db_product = result.scalars().first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(db_product)
    await db.commit()
    return db_product

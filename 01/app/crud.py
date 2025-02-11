from sqlalchemy.orm import Session
from .models import Product, Category
from .schemas import ProductCreate ,CategoryInput


def get_products(db: Session):
    return db.query(Product).all()


def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        name=product.name, description=product.description, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def generate_dummy_data(db: Session):
    for i in range(1, 10001):
        product = Product(
            name=f"Product {i}", description=f"Description {i}", price=i * 10.0)
        db.add(product)
    db.commit()


from slugify import slugify

def create_category(db: Session, category: CategoryInput):
    # Convert Pydantic model to SQLAlchemy model
    category_data = category.dict()
    category_data['slug'] = slugify(category_data['name'])  # Generate slug from name
    db_category = Category(**category_data)  # Create Category instance
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


from . import models, schemas

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

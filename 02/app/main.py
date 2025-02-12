from fastapi import FastAPI
from auth.api import router as auth_router
from app.db import engine
from auth.models import Base

app = FastAPI()

# Database Initialization
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await init_db()

# Register Routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from auth.models import User
from auth.security import hash_password
from auth.schemas import UserCreate


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # ✅ Convert UUID to string
    return UserResponse(id=str(db_user.id), email=db_user.email)

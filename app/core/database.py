from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


class Base(DeclarativeBase):
    """Base declarative class for all SQLAlchemy models."""
    pass


# Create async SQLAlchemy engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    # Connect args specific to SQLite to enable WAL mode & busy timeout
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def init_db() -> None:
    """Initialize database tables and seed demo user for serverless environments."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        from sqlalchemy import select
        from app.models.user import User
        from app.core.security import get_password_hash

        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.email == "demo@fastapi.dev"))
            if not result.scalars().first():
                demo_user = User(
                    id=1,
                    email="demo@fastapi.dev",
                    full_name="Demo Showcase User",
                    hashed_password=get_password_hash("secret123"),
                    is_active=True,
                    is_superuser=False
                )
                session.add(demo_user)
                await session.commit()
    except Exception as e:
        print("Init DB seed notice:", e)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that yields a database session per request."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

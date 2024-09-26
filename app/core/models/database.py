from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base


SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
AsyncSessionLocal = AsyncSession(autocommit=False,
                                 autoflush=False, bind=engine)

Base = declarative_base()

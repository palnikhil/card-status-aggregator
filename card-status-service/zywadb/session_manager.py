import logging
import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


class DbSessionManager:

    def __init__(self, db_user, db_user_pass, db_host, db_port, db_name,
                 pool_size=10,
                 max_overflow=20):
        self._db_user = db_user
        self._db_user_pass = db_user_pass
        self._db_host = db_host
        self._db_port = db_port
        self._db_name = db_name
        self._pool_size = pool_size
        self._max_overflow = max_overflow
        self._session = None
        self._init_db()

    @classmethod
    def from_env(cls):
        db_user = os.getenv('DB_USER')
        db_user_pass = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')
        pool_size = int(os.getenv('DB_POOL_SIZE', 5))  # default to 5 if not set
        max_overflow = int(os.getenv('DB_MAX_OVERFLOW', 10))  # default to 10 if not set
        return cls(db_user, db_user_pass, db_host, db_port, db_name, pool_size, max_overflow)

    def _init_db(self):
        _db_url = f'postgresql+asyncpg://{self._db_user}:{self._db_user_pass}@{self._db_host}:{self._db_port}/{self._db_name}'
        print(_db_url)
        engine = create_async_engine(_db_url, echo=True, pool_size=self._pool_size, max_overflow=self._max_overflow)
        self._session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        logger.info('Database session manager initialized')

    def session(self) -> AsyncSession:
        return self._session()
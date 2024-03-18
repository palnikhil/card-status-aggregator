import logging
from contextlib import asynccontextmanager
from functools import wraps
from typing import AsyncContextManager, Any, Optional
from typing import Callable

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .session_manager import DbSessionManager

logger = logging.getLogger(__name__)


class DBService:

    def __init__(self, session_manager: DbSessionManager, schema_resolver: Callable[..., Any] = None):
        self._session_manager = session_manager
        self._schema_resolver = schema_resolver

    @staticmethod
    def db_session(schema_override: Optional[str] = 'public'):
        def decorator(func):
            @wraps(func)
            async def wrapper(self, *args, **kwargs):
                schema = schema_override if schema_override is not None else self._schema_resolver(*args, **kwargs)
                async with self.session_scope(schema) as session:
                    self.session = session
                    return await func(self, session, *args, **kwargs)
            return wrapper
        return decorator

    @asynccontextmanager
    async def session_scope(self, schema: str) -> AsyncContextManager[AsyncSession]: # type: ignore
        session = self._session_manager.session()
        await session.execute(text(f'SET search_path TO {schema}'))
        logger.info(f'Starting session for schema {schema}')
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

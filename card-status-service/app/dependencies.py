import os
from functools import lru_cache
from zywadb import DbSessionManager

from .services.db.card_status_db_service import CardStatusDbService

_db_session_manager = DbSessionManager.from_env()

@lru_cache()
def get_card_status_db_service() -> CardStatusDbService:
    return CardStatusDbService(_db_session_manager)
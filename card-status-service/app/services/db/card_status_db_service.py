import logging

from typing import Optional

from zywadb import DBService, DbSessionManager

from sqlalchemy import select, and_, text, desc
from sqlalchemy.orm import joinedload

from app.models.card_status_model import CardStatusEventModel
from app.models.schema import CardStatusEvent

logger = logging.getLogger(__name__)

class CardStatusDbService(DBService):

    def __init__(self, session_manager: DbSessionManager):
        super().__init__(
            session_manager
        )

    @DBService.db_session()
    async def get_card_status(
        self, session, card_id: str
    ) -> Optional[CardStatusEvent]:
        logger.info(f"Getting card status for the card {card_id}")
        result = await session.execute(
            select(CardStatusEventModel)
            .where(CardStatusEventModel.card_id == card_id)
            .order_by(desc(CardStatusEventModel.timestamp))
            .limit(1)
        )
        maybe_event = result.scalars().first()
        if maybe_event:
            return CardStatusEvent.from_orm(maybe_event)

    @DBService.db_session()
    async def is_ready(self, session) -> bool:
        logger.info("Checking if service is ready")
        result = await session.execute(text("SELECT 1"))
        assert (
            result.scalar() == 1
        ), "Unexpected result from database health check query"
        return True



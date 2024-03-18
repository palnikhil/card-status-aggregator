from typing import Optional
from datetime import datetime
from pydantic import BaseModel


from app.models.card_status_model import CardStatusEventModel

class CardStatusEvent(BaseModel):
    id: int
    card_id: str
    user_contact: str
    timestamp: datetime
    status: str
    comment: Optional[str] = None

    @staticmethod
    def from_orm(event_model: CardStatusEventModel) -> "CardStatusEvent":
        return CardStatusEvent(
            id=event_model.id,
            card_id=event_model.card_id,
            user_contact=event_model.user_contact,
            timestamp=event_model.timestamp,
            status=event_model.status,
            comment=event_model.comment
        )

    def to_orm(self) -> CardStatusEventModel:
        return CardStatusEventModel(
            id=self.id,
            card_id=self.card_id,
            user_contact=self.user_contact,
            timestamp=self.timestamp,
            status=self.status,
            comment=self.comment
        )
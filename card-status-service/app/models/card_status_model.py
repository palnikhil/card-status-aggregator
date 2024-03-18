from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CardStatusEventModel(Base):
    __tablename__ = 'card_status_events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    card_id = Column(String(255), nullable=False)
    user_contact = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    status = Column(String(255), nullable=False)
    comment = Column(Text, nullable=True)
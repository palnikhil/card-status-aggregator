import logging

from fastapi import Depends
from fastapi import FastAPI, HTTPException

from app.services.db.card_status_db_service import CardStatusDbService

from .dependencies import get_card_status_db_service

app = FastAPI()

log = logging.getLogger(__name__)

@app.get("/live")
async def live():
    log.info("[Health check][live]")
    return {"status": "UP"}

@app.get("/{card_id}")
async def get_card_status_by_id(
    card_id: str,
    card_status_db_service: CardStatusDbService = Depends(get_card_status_db_service),
):
    log.info(
        f"Getting status for card {card_id}"
    )
    invoice = await card_status_db_service.get_card_status(
        card_id=card_id
    )
    if not invoice:
        raise HTTPException(
            status_code=404, detail=f"Card {card_id} not found")

    return invoice
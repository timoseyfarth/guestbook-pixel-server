from typing import List
from fastapi import APIRouter, Depends, Security, Response
from sqlmodel import Session

from database import get_session
from auth import get_api_key
from models import GuestbookEntryCreate, GuestbookEntryResponse
from service import GuestbookService
from logger import setup_logger

router = APIRouter(prefix="/github-guestbook", tags=["guestbook"])
logger = setup_logger()


@router.post("/register", response_model=GuestbookEntryResponse) #TODO rate limiting
def register_guestbook(
        entry: GuestbookEntryCreate,
        session: Session = Depends(get_session),
        api_key: str = Security(get_api_key)
):
    logger.info(f"New Guestbook Signer: {entry.username}")
    logger.info(f"Avatar URL: {entry.avatar_url}")
    logger.info(f"Favorite Editor: {entry.editor}")
    logger.info(f"Quote: {entry.quote}")
    logger.info(f"Color: {entry.mood_color}")

    db_entry = GuestbookService.add_entry(session, entry) # TODO  return proper message to the client
    return db_entry


# @router.get("/entries", response_model=List[GuestbookEntryResponse])
# def get_all_entries(
#         session: Session = Depends(get_session),
#         api_key: str = Security(get_api_key)
# ):
#     return GuestbookService.get_all_entries(session)
#
#
# @router.get("/entries/{username}", response_model=GuestbookEntryResponse)
# def get_entry(
#         username: str,
#         session: Session = Depends(get_session),
#         api_key: str = Security(get_api_key)
# ):
#     entry = GuestbookService.get_entry_by_username(session, username)
#     if not entry:
#         from fastapi import HTTPException, status
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User '{username}' not found"
#         )
#     return entry
#
#
# @router.put("/entries/{username}", response_model=GuestbookEntryResponse)
# def update_entry(
#         username: str,
#         entry: GuestbookEntryCreate,
#         session: Session = Depends(get_session),
#         api_key: str = Security(get_api_key)
# ):
#     """Update an existing guestbook entry"""
#     logger.info(f"Updating Guestbook Entry: {username}")
#     return GuestbookService.update_entry(session, username, entry)
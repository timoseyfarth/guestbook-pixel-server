import os
from typing import List
from fastapi import APIRouter, Depends, Security, Response
from sqlmodel import Session

from database import get_session
from auth import get_api_key
from models import GuestbookEntryCreate, GuestbookEntryResponse
from guestbook_service import GuestbookService
from logger import logger
from pixelgrid import gen_and_save_svg

STATIC_ASSETS_PATH = os.getenv("STATIC_ASSETS_PATH", "debug")
STATIC_SVG_FILE = os.getenv("STATIC_SVG_FILE", "file.svg")

SVG_OUTPUT = os.path.join(STATIC_ASSETS_PATH, STATIC_SVG_FILE)
if STATIC_ASSETS_PATH:
    os.makedirs(STATIC_ASSETS_PATH, exist_ok=True)

router = APIRouter(prefix="/github-guestbook", tags=["guestbook"])

@router.post("/register", response_model=GuestbookEntryResponse) #TODO rate limiting
def register_guestbook(
        entry: GuestbookEntryCreate,
        session: Session = Depends(get_session),
        api_key: str = Security(get_api_key)
):
    logger.info(f"New Guestbook Signer Requested {entry.username}")

    entry_response = GuestbookService.add_entry(session, entry)
    all_entries = GuestbookService.get_all_entries(session)
    
    result = gen_and_save_svg(all_entries, SVG_OUTPUT)

    entry_response.message += result
    entry_response.message += f"[Go to the pixel grid.](https://github.com/timoseyfarth)"
    
    return entry_response

@router.get("/health")
def health_check():
    return {"status": "healthy"}


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
from datetime import datetime
from typing import Optional, List
from sqlmodel import Session, select
from fastapi import HTTPException, status

from color import get_dominant_color, get_random_hex
from models import GuestbookEntry, GuestbookEntryCreate, GuestbookEntryResponse, GuestbookEntryInsert
from logger import logger


class GuestbookService:
    @staticmethod
    def get_entry_by_username(session: Session, username: str) -> Optional[GuestbookEntry]:
        statement = select(GuestbookEntry).where(GuestbookEntry.username == username)
        return session.exec(statement).first()

    @staticmethod
    def get_all_entries(session: Session) -> List[GuestbookEntry]:
        statement = select(GuestbookEntry).order_by(GuestbookEntry.created_at)
        return list(session.exec(statement).all())

    @staticmethod
    def add_entry(session: Session, entry_data: GuestbookEntryCreate) -> GuestbookEntryResponse:
        entry_import = GuestbookEntryInsert(
            username=entry_data.username,
            avatar_url=entry_data.avatar_url,
            avatar_hex=get_random_hex(),
            editor=entry_data.editor,
            quote=entry_data.quote,
            mood_color=entry_data.mood_color,
            is_anonymous=entry_data.is_anonymous
        )
        message = ""

        try:
            entry_import.avatar_hex = get_dominant_color(entry_data.avatar_url)
        except Exception as e:
            logger.error(f"Failed to extract dominant color for {entry_data.username}: {e}")
            message += f"Failed to extract dominant color. Using random color instead. "

        existing_entry = GuestbookService.get_entry_by_username(session, entry_data.username)

        if existing_entry:
            new_entry = GuestbookService.update_entry(session, entry_data.username, entry_import)
            message += "🔄 You already claimed a pixel. It was successfully updated. "
        else:
            new_entry = GuestbookService.create_entry(session, entry_import)
            message += "✅ Pixel added successfully. "

        return GuestbookEntryResponse(
            id=new_entry.id,
            username=new_entry.username,
            avatar_url=new_entry.avatar_url,
            avatar_hex=new_entry.avatar_hex,
            editor=new_entry.editor,
            quote=new_entry.quote,
            mood_color=new_entry.mood_color,
            is_anonymous=new_entry.is_anonymous,
            created_at=new_entry.created_at,
            updated_at=new_entry.updated_at,
            message=message,
        )

    @staticmethod
    def create_entry(session: Session, entry_data: GuestbookEntryInsert) -> GuestbookEntry:
        db_entry = GuestbookEntry(
            username=entry_data.username,
            avatar_url=entry_data.avatar_url,
            avatar_hex=entry_data.avatar_hex,
            is_anonymous=entry_data.is_anonymous,
            editor=entry_data.editor,
            quote=entry_data.quote,
            mood_color=entry_data.mood_color
        )

        session.add(db_entry)
        session.commit()
        session.refresh(db_entry)

        logger.info(f"Successfully created new guestbook entry for user: {db_entry.username}")
        return db_entry

    @staticmethod
    def update_entry(session: Session, username: str, entry_data: GuestbookEntryInsert) -> GuestbookEntry:
        db_entry = GuestbookService.get_entry_by_username(session, username)
        if not db_entry:
            logger.warning(f"Update failed: User '{username}' not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User '{username}' not found"
            )

        db_entry.avatar_url = entry_data.avatar_url
        db_entry.avatar_hex = entry_data.avatar_hex
        db_entry.editor = entry_data.editor
        db_entry.quote = entry_data.quote
        db_entry.mood_color = entry_data.mood_color
        db_entry.is_anonymous = entry_data.is_anonymous
        db_entry.updated_at = datetime.now()

        session.commit()
        session.refresh(db_entry)

        logger.info(f"Successfully updated guestbook entry for user: {username}")
        return db_entry

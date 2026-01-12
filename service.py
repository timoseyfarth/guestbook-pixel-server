from datetime import datetime
from typing import Optional, List
from sqlmodel import Session, select
from fastapi import HTTPException, status

from models import GuestbookEntry, GuestbookEntryCreate, GuestbookEntryResponse


class GuestbookService:
    @staticmethod
    def get_entry_by_username(session: Session, username: str) -> Optional[GuestbookEntry]:
        statement = select(GuestbookEntry).where(GuestbookEntry.username == username)
        return session.exec(statement).first()

    # @staticmethod
    # def get_all_entries(session: Session) -> List[GuestbookEntry]:
    #     statement = select(GuestbookEntry).order_by(GuestbookEntry.created_at.desc())
    #     return list(session.exec(statement).all())

    @staticmethod
    def add_entry(session: Session, entry_data: GuestbookEntryCreate) -> GuestbookEntry:
        existing_entry = GuestbookService.get_entry_by_username(session, entry_data.username)

        if existing_entry: # TODO return if new enry or updated
            return GuestbookService.update_entry(session, entry_data.username, entry_data)
        else:
            return GuestbookService.create_entry(session, entry_data)

    @staticmethod
    def create_entry(session: Session, entry_data: GuestbookEntryCreate) -> GuestbookEntry:
        db_entry = GuestbookEntry(
            username=entry_data.username,
            avatar_url=entry_data.avatar_url,
            editor=entry_data.editor,
            quote=entry_data.quote,
            mood_color=entry_data.mood_color
        )

        session.add(db_entry)
        session.commit()
        session.refresh(db_entry)

        return db_entry

    @staticmethod
    def update_entry(session: Session, username: str, entry_data: GuestbookEntryCreate) -> GuestbookEntry:
        db_entry = GuestbookService.get_entry_by_username(session, username)
        if not db_entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User '{username}' not found"
            )

        db_entry.avatar_url = entry_data.avatar_url
        db_entry.editor = entry_data.editor
        db_entry.quote = entry_data.quote
        db_entry.mood_color = entry_data.mood_color
        db_entry.updated_at = datetime.now()

        session.commit()
        session.refresh(db_entry)

        return db_entry

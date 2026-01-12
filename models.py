from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class GuestbookEntry(SQLModel, table=True):
    __tablename__ = "guestbook_entries"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    avatar_url: str
    editor: Optional[str] = None
    quote: Optional[str] = None
    mood_color: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class GuestbookEntryCreate(SQLModel):
    username: str
    avatar_url: str
    editor: Optional[str] = None
    quote: Optional[str] = None
    mood_color: Optional[str] = None


class GuestbookEntryResponse(SQLModel):
    id: int
    username: str
    avatar_url: str
    editor: Optional[str] = None
    quote: Optional[str] = None
    mood_color: Optional[str] = None
    created_at: datetime
    updated_at: datetime
import humanize
from hive.core.extensions import db
from sqlalchemy import DateTime, String, Integer, ForeignKey, Text
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Mapped, mapped_column

class Message(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default= lambda: datetime.now(timezone.utc), index=True)

    def time_since_creation(self) -> timedelta:
        created_at_tz_aware = self.created_at.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        td = now - created_at_tz_aware
        return td
    
    def convert_td_to_str(td: timedelta) -> str:
        return humanize.naturaldelta(td)
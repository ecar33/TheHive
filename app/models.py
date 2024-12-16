import humanize
from app.extensions import db
from sqlalchemy import DateTime, String, Integer, ForeignKey
from datetime import datetime, timedelta, timezone

class Message(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)
    content = db.Column(String)
    created_at = db.Column(DateTime, default=datetime.now(timezone.utc))

    def time_since_creation(self) -> timedelta:
        created_at_tz_aware = self.created_at.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        td = now - created_at_tz_aware
        return td
    
    def convert_td_to_str(td: timedelta) -> str:
        return humanize.naturaldelta(td)
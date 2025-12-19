from flask_login import UserMixin
from hive.core.extensions import db, bcrypt
from sqlalchemy import String, Text
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

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128)) 
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def set_profile_picture(self, path):
        self.profile_picture = path
    
    def validate_password(self, input_password):
        return bcrypt.check_password_hash(self.password, input_password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
        }
    
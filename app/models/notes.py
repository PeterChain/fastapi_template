from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Note(Base):
    __tablename__ = "note"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, index=True)
    detail = Column(String)
    user_id = Column(String, ForeignKey("user.username"))




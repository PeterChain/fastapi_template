from sqlalchemy import Column, Boolean, String


from ..database import Base


class User(Base):
    __tablename__ = "user"

    username = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String)
    hashed_password = Column(String)
    active = Column(Boolean)
    admin = Column(Boolean, default=False)
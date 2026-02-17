from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    wallet = relationship(
        "Wallet", back_populates="owner", uselist=False, cascade="all, delete-orphan"
    )
    # games = relationship("BlackjackGame", back_populates="player")

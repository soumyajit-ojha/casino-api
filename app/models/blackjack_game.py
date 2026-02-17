from sqlalchemy import Column, Integer, Float, String, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base


class BlackjackGame(Base):
    __tablename__ = "blackjack_games"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bet_amount = Column(Float, nullable=False)

    # Stored as lists of strings, e.g., ["A", "10"]
    player_hand = Column(JSON, default=list, nullable=False)
    dealer_hand = Column(JSON, default=list, nullable=False)

    # Statuses: active, player_win, dealer_win, push, blackjack, player_bust
    status = Column(String, default="active", nullable=False)
    is_over = Column(Boolean, default=False, nullable=False)

    # Link back to user
    player = relationship("User", back_populates="games")

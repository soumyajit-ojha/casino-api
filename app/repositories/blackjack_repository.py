from sqlalchemy.orm import Session
from app.models.blackjack_game import BlackjackGame
from typing import Optional, List


class BlackjackRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, game: BlackjackGame) -> BlackjackGame:
        self.db.add(game)
        self.db.flush()  # Get the ID before committing
        return game

    def get_by_id(self, game_id: int) -> Optional[BlackjackGame]:
        return self.db.query(BlackjackGame).filter(BlackjackGame.id == game_id).first()

    def get_active_game(self, user_id: int) -> Optional[BlackjackGame]:
        """Check if the user has an unfinished game."""
        return (
            self.db.query(BlackjackGame)
            .filter(BlackjackGame.user_id == user_id, BlackjackGame.is_over == False)
            .first()
        )

    def get_user_history(self, user_id: int, limit: int = 10) -> List[BlackjackGame]:
        return (
            self.db.query(BlackjackGame)
            .filter(BlackjackGame.user_id == user_id)
            .order_by(BlackjackGame.id.desc())
            .limit(limit)
            .all()
        )

    def update(self, game: BlackjackGame) -> BlackjackGame:
        """
        Updates the game state.
        Note: The transaction commit is usually handled by the Service layer.
        """
        self.db.add(game)
        self.db.flush()
        return game

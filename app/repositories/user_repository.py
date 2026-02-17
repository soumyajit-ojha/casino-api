from sqlalchemy.orm import Session
from app.models.user import User

from app.models.wallet import Wallet


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def create_user_with_wallet(self, username: str, hashed_password: str) -> User:
        """
        Creates both User and Wallet in a single transaction.
        Essential for Blackjack gameplay logic.
        """
        new_user = User(username=username, hashed_password=hashed_password)
        self.db.add(new_user)
        self.db.flush()  # Obtain new_user.id without committing yet

        # Initialize wallet with a starting balance (e.g., 1000 units)
        new_wallet = Wallet(user_id=new_user.id, balance=1000.0)
        self.db.add(new_wallet)

        self.db.commit()
        self.db.refresh(new_user)
        return new_user

from sqlalchemy.orm import Session
from app.models.wallet import Wallet


class WalletRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: int) -> Wallet:
        return self.db.query(Wallet).filter(Wallet.user_id == user_id).first()

    def get_by_user_id_for_update(self, user_id: int) -> Wallet:
        """
        Locks the wallet row for the current transaction.
        Crucial for preventing double-spending in concurrent games.
        """
        return (
            self.db.query(Wallet)
            .filter(Wallet.user_id == user_id)
            .with_for_update()
            .first()
        )

    def update(self, wallet: Wallet) -> Wallet:
        self.db.add(wallet)
        # Flush ensures changes are sent to DB but transaction remains open for service logic
        self.db.flush()
        return wallet

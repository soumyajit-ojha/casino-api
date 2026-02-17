from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.wallet_repository import WalletRepository
from app.models.wallet import Wallet


class WalletService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = WalletRepository(db)

    def get_user_balance(self, user_id: int) -> Wallet:
        wallet = self.repo.get_by_user_id(user_id)
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        return wallet

    def deposit(self, user_id: int, amount: float) -> Wallet:
        """Atomic deposit operation."""
        wallet = self.repo.get_by_user_id_for_update(user_id)
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")

        wallet.balance += amount
        self.repo.update(wallet)
        self.db.commit()
        self.db.refresh(wallet)
        return wallet

    def deduct_funds(self, user_id: int, amount: float) -> Wallet:
        """
        Securely deduct funds. This should be called by the Blackjack Service.
        Note: We don't commit here if this is part of a larger game transaction.
        """
        wallet = self.repo.get_by_user_id_for_update(user_id)
        if wallet.balance < amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds"
            )

        wallet.balance -= amount
        self.repo.update(wallet)
        return wallet

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.endpoints import deps
from app.schemas.wallet_schema import WalletResponse, WalletDeposit
from app.services.wallet_service import WalletService
from app.models.user import User

router = APIRouter()


@router.get("/me", response_model=WalletResponse)
def get_my_balance(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    service = WalletService(db)
    wallet = service.get_user_balance(current_user.id)
    return {"success": True, "message": "Balance retrieved", "data": wallet}


@router.post("/deposit", response_model=WalletResponse)
def deposit_funds(
    payload: WalletDeposit,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """Simple endpoint to add funds for testing/demo."""
    service = WalletService(db)
    wallet = service.deposit(current_user.id, payload.amount)
    return {
        "success": True,
        "message": f"Successfully deposited {payload.amount}",
        "data": wallet,
    }

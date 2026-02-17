from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class WalletBase(BaseModel):
    balance: float = Field(..., ge=0)


class WalletDeposit(BaseModel):
    amount: float = Field(..., gt=0, description="Amount to add to wallet")


class WalletOut(WalletBase):
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class WalletResponse(BaseModel):
    success: bool
    data: Optional[WalletOut] = None
    message: str

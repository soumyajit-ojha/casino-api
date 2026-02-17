from pydantic import BaseModel, Field, ConfigDict
from typing import List, Union, Optional


class GameStartRequest(BaseModel):
    bet_amount: float = Field(..., gt=0, description="The amount you want to wager")


class GameData(BaseModel):
    game_id: int
    player_hand: List[str]
    dealer_hand: List[
        str
    ]  # This will contain ["hidden"] or actual cards based on state
    player_score: int
    dealer_score: Optional[int] = None
    status: str
    is_over: bool
    bet_amount: float

    model_config = ConfigDict(from_attributes=True)


class GameResponse(BaseModel):
    success: bool
    data: Optional[GameData] = None
    message: Optional[str] = None

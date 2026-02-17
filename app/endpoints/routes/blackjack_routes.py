from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.endpoints import deps
from app.schemas.blackjack_schema import GameStartRequest, GameResponse
from app.services.blackjack_service import BlackjackService
from app.models.user import User

router = APIRouter()


@router.post("/start", response_model=GameResponse)
def start_game(
    payload: GameStartRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    service = BlackjackService(db)
    game = service.start_game(current_user.id, payload.bet_amount)
    data = service.get_game_state_formatted(game)

    return {
        "success": True,
        "message": "Game started" if not game.is_over else f"Game ended: {game.status}",
        "data": data,
    }


@router.post("/{game_id}/hit", response_model=GameResponse)
def hit(
    game_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    service = BlackjackService(db)
    game = service.hit(current_user.id, game_id)
    data = service.get_game_state_formatted(game)

    return {
        "success": True,
        "message": "Player draws a card" if not game.is_over else "Player busted",
        "data": data,
    }


@router.post("/{game_id}/stand", response_model=GameResponse)
def stand(
    game_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    service = BlackjackService(db)
    game = service.stand(current_user.id, game_id)
    data = service.get_game_state_formatted(game)

    return {"success": True, "message": f"Game settled: {game.status}", "data": data}


@router.get("/{game_id}", response_model=GameResponse)
def get_game(
    game_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    service = BlackjackService(db)
    game = service.repo.get_by_id(game_id)
    if not game or game.user_id != current_user.id:
        return {"success": False, "message": "Game not found", "data": None}

    data = service.get_game_state_formatted(game)
    return {"success": True, "data": data}

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.blackjack_repository import BlackjackRepository
from app.repositories.wallet_repository import WalletRepository
from app.services.blackjack_engine import BlackjackEngine
from app.models.blackjack_game import BlackjackGame
from app.schemas.blackjack_schema import GameData


class BlackjackService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = BlackjackRepository(db)
        self.wallet_repo = WalletRepository(db)
        self.engine = BlackjackEngine()

    def start_game(self, user_id: int, bet_amount: float) -> BlackjackGame:
        # 1. Check for existing active game
        if self.repo.get_active_game(user_id):
            raise HTTPException(
                status_code=400, detail="Finish your current game first"
            )

        # 2. Lock wallet and deduct funds (Pessimistic lock via Repository)
        wallet = self.wallet_repo.get_by_user_id_for_update(user_id)
        if not wallet or wallet.balance < bet_amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        wallet.balance -= bet_amount

        # 3. Deal initial hands
        p_hand, d_hand = self.engine.get_initial_deal()

        game = BlackjackGame(
            user_id=user_id,
            bet_amount=bet_amount,
            player_hand=p_hand,
            dealer_hand=d_hand,
            status="active",
            is_over=False,
        )

        # 4. Immediate Blackjack check (Natural 21)
        if self.engine.is_blackjack(p_hand):
            self._settle_game(game, wallet, "blackjack")

        self.repo.create(game)
        self.db.commit()  # Atomic: bet deducted and game created together
        return game

    def hit(self, user_id: int, game_id: int) -> BlackjackGame:
        game = self.repo.get_by_id(game_id)
        if not game or game.user_id != user_id or game.is_over:
            raise HTTPException(
                status_code=400, detail="Invalid game or game already finished"
            )

        # Draw card
        game.player_hand.append(self.engine.draw_card())

        # Check if player busted
        if self.engine.calculate_score(game.player_hand) > 21:
            wallet = self.wallet_repo.get_by_user_id_for_update(user_id)
            self._settle_game(game, wallet, "dealer_win")

        self.db.commit()
        return game

    def stand(self, user_id: int, game_id: int) -> BlackjackGame:
        game = self.repo.get_by_id(game_id)
        if not game or game.user_id != user_id or game.is_over:
            raise HTTPException(status_code=400, detail="Invalid game state")

        # Dealer takes their turn
        game.dealer_hand = self.engine.dealer_play(game.dealer_hand)

        # Determine result
        result = self.engine.determine_result(game.player_hand, game.dealer_hand)

        # Settle funds
        wallet = self.wallet_repo.get_by_user_id_for_update(user_id)
        self._settle_game(game, wallet, result)

        self.db.commit()
        return game

    def _settle_game(self, game: BlackjackGame, wallet, result: str):
        """Internal helper to calculate payouts and close game."""
        game.status = result
        game.is_over = True

        payout = 0
        if result == "blackjack":
            payout = game.bet_amount * 2.5  # 3 to 2 payout + original bet
        elif result == "player_win":
            payout = game.bet_amount * 2  # Double the bet
        elif result == "push":
            payout = game.bet_amount  # Return original bet

        if payout > 0:
            wallet.balance += payout

    def get_game_state_formatted(self, game: BlackjackGame) -> dict:
        """Logic to hide dealer's second card if game is active."""
        dealer_hand = game.dealer_hand
        dealer_score = None

        if not game.is_over:
            # Hide second card for player
            dealer_hand = [game.dealer_hand[0], "??"]
            dealer_score = self.engine.calculate_score([game.dealer_hand[0]])
        else:
            dealer_score = self.engine.calculate_score(game.dealer_hand)

        return {
            "game_id": game.id,
            "player_hand": game.player_hand,
            "dealer_hand": dealer_hand,
            "player_score": self.engine.calculate_score(game.player_hand),
            "dealer_score": dealer_score,
            "status": game.status,
            "is_over": game.is_over,
            "bet_amount": game.bet_amount,
        }

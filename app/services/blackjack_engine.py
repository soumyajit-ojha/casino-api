import secrets
from typing import List, Tuple


class BlackjackEngine:
    """
    Pure logic class for Blackjack rules.
    This class handles scoring, card drawing, and dealer AI.
    It does not interact with the database.
    """

    # Standard 52-card deck representation (simplified to ranks)
    CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    # Card values mapping
    CARD_VALUES = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 10,
        "Q": 10,
        "K": 10,
        "A": 11,
    }

    @classmethod
    def draw_card(cls) -> str:
        """Draws a single card rank using cryptographically secure RNG."""
        return secrets.choice(cls.CARDS)

    @classmethod
    def calculate_score(cls, hand: List[str]) -> int:
        """
        Calculates the best possible score for a given hand.
        Correctly handles Aces being 1 or 11.
        """
        score = sum(cls.CARD_VALUES[card] for card in hand)

        # Count Aces to adjust if score > 21
        aces = hand.count("A")

        # If score is over 21 and we have aces, convert 11s to 1s
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1

        return score

    @classmethod
    def is_blackjack(cls, hand: List[str]) -> bool:
        """Returns True if the initial 2-card hand is exactly 21."""
        return len(hand) == 2 and cls.calculate_score(hand) == 21

    @classmethod
    def dealer_play(cls, current_hand: List[str]) -> List[str]:
        """
        Standard Dealer AI:
        Dealer must hit until their score is at least 17.
        """
        hand = list(current_hand)  # Work on a copy to maintain purity

        while cls.calculate_score(hand) < 17:
            hand.append(cls.draw_card())

        return hand

    @classmethod
    def determine_result(cls, player_hand: List[str], dealer_hand: List[str]) -> str:
        """
        Determines the game outcome status.
        Returns: 'player_win', 'dealer_win', 'push', or 'blackjack'
        """
        p_score = cls.calculate_score(player_hand)
        d_score = cls.calculate_score(dealer_hand)

        # 1. Player Bust
        if p_score > 21:
            return "dealer_win"

        # 2. Dealer Bust
        if d_score > 21:
            return "player_win"

        # 3. Score Comparison
        if p_score > d_score:
            return "player_win"
        elif d_score > p_score:
            return "dealer_win"
        else:
            return "push"

    @classmethod
    def get_initial_deal(cls) -> Tuple[List[str], List[str]]:
        """Utility to deal the starting 2 cards for both parties."""
        player_hand = [cls.draw_card(), cls.draw_card()]
        dealer_hand = [cls.draw_card(), cls.draw_card()]
        return player_hand, dealer_hand

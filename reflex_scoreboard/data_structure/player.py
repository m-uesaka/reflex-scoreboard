from dataclasses import dataclass
from enum import Enum


class PlayerState(Enum):
    """Enumeration for player states."""

    NORMAL = 0
    WIN = 1
    LOSE = -1


@dataclass
class PlayerScore:
    """Base class for player scores.

    Attributes:
        player_id (str): Unique identifier for the player.
        name (str): Name of the player.
        answers (int): Number of correct answers. Default to 0.
        misses (int): Number of misses. Default to 0.
        score (int): Total score. Default to 0.
        breaks (int): Number of breaks. Default to 0.
        state (PlayerState): Current state of the player. Default to PlayerState.NORMAL.

    """

    player_id: int
    name: str
    answers: int = 0
    misses: int = 0
    score: int = 0
    breaks: int = 0
    state: PlayerState = PlayerState.NORMAL

    def is_same_player(self, player: "PlayerScore") -> bool:
        """Check if the current player is the same as another player.

        Args:
            player (PlayerScore): The player to compare with.

        Returns:
            bool: True if the players are the same, False otherwise.

        """
        return self.player_id == player.player_id and self.name == player.name

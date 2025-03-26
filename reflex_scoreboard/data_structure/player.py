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

    def __eq__(self, other: object) -> bool:
        """Check equality based on player_id and name.

        Args:
            other (object): The object to compare with.

        Raises:
            NotImplemented: If the other object is not an instance of PlayerScore.

        Returns:
            bool: True if equal, False otherwise.

        """
        if not isinstance(other, PlayerScore):
            raise NotImplementedError("Other must be an instance of PlayerScore.")
        return self.player_id == other.player_id and self.name == other.name

import dataclasses
from enum import Enum


class PlayerState(Enum):
    """Enumeration for player states."""

    NORMAL = 0
    WIN = 1
    LOSE = -1


@dataclasses.dataclass(frozen=True)
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

    def add_answer(self) -> "PlayerScore":
        """Increment the number of correct answers by 1.

        Returns:
            PlayerScore: A new PlayerScore instance with incremented answers.

        """
        return dataclasses.replace(self, answers=self.answers + 1)

    def add_miss(self) -> "PlayerScore":
        """Increment the number of misses by 1.

        Returns:
            PlayerScore: A new PlayerScore instance with incremented misses.

        """
        return dataclasses.replace(self, misses=self.misses + 1)

    def update_score(self, score: int) -> "PlayerScore":
        """Update the score of the player.

        Args:
            score (int): The new score to set.

        Returns:
            PlayerScore: A new PlayerScore instance with updated score.

        """
        return dataclasses.replace(self, score=score)

    def set_breaks(self, breaks: int) -> "PlayerScore":
        """Update the number of breaks for the player.

        Args:
            breaks (int): The new number of breaks to set.

        Returns:
            PlayerScore: A new PlayerScore instance with updated breaks.

        """
        return dataclasses.replace(self, breaks=breaks)

    def update_state(self, state: PlayerState) -> "PlayerScore":
        """Update the state of the player.

        Args:
            state (PlayerState): The new state to set.

        Returns:
            PlayerScore: A new PlayerScore instance with updated state.

        """
        return dataclasses.replace(self, state=state)

    def is_same_player(self, player: "PlayerScore") -> bool:
        """Check if the current player is the same as another player.

        Args:
            player (PlayerScore): The player to compare with.

        Returns:
            bool: True if the players are the same, False otherwise.

        """
        return self.player_id == player.player_id and self.name == player.name

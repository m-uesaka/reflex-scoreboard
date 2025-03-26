import itertools
from dataclasses import dataclass

from reflex_scoreboard.data_structure.player import PlayerScore


@dataclass
class ScoreboardState:
    """The dataclass to store the scoreboard state.

    Attributes:
        players (list[PlayerScore]): List of PlayerScore objects.
        question_count (int): Number of questions. Default to 1.

    """

    players: list[PlayerScore]
    question_count: int = 1

    def __post_init__(self) -> None:
        """Validate the players list."""
        # Ensure all players are different
        for player1, player2 in itertools.combinations(self.players, 2):
            if player1 == player2:
                raise ValueError("Players must be different.")
        if self.question_count < 1:
            raise ValueError("Question count must be at least 1.")

    def __getitem__(self, index: int) -> PlayerScore:
        """Get the player at the given index.

        Args:
            index (int): The index of the player to retrieve.

        Returns:
            PlayerScore: The player at the given index.

        """
        if index < 0 or index >= len(self.players):
            raise IndexError("Index out of range.")
        return self.players[index]

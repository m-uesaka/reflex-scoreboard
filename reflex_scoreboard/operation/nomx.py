from reflex_scoreboard.data_structure.payload import Payload
from reflex_scoreboard.data_structure.player import PlayerState
from reflex_scoreboard.data_structure.scoreboard import ScoreboardState
from reflex_scoreboard.operation.operation_base import OperationBase


class NoMxOperation(OperationBase):
    """Class for handling NoMx operations on the scoreboard.

    Attributes:
        win_threshold (int): The threshold for winning.
        lose_threshold (int): The threshold for losing.

    """

    def __init__(self, win_threshold: int, lose_threshold: int) -> None:
        """Initialize the NoMxOperation with win and lose thresholds.

        Args:
            win_threshold (int): The threshold for winning.
            lose_threshold (int): The threshold for losing.

        Raises:
            ValueError: If win_threshold or lose_threshold is less than or equal to 0.

        """
        if win_threshold <= 0:
            raise ValueError("Win threshold must be positive.")
        if lose_threshold <= 0:
            raise ValueError("Lose threshold must be positive.")

        self.win_threshold = win_threshold
        self.lose_threshold = lose_threshold

    def answer_right(self, scoreboard: ScoreboardState, index: int) -> ScoreboardState:
        """Perform the answer right operation on the scoreboard.

        Args:
            scoreboard (ScoreboardState): The scoreboard state.
            index (int): The index of the player who answered correctly.

        Returns:
            ScoreboardState: The updated scoreboard state with the correct answer.

        """
        new_scoreboard = type(self).add_answers(scoreboard, index)
        if new_scoreboard[index].answers >= self.win_threshold:
            new_scoreboard[index].state = PlayerState.WIN
        new_scoreboard.question_count += 1
        return new_scoreboard

    def make_miss(self, scoreboard: ScoreboardState, index: int) -> ScoreboardState:
        """Perform the make miss operation on the scoreboard.

        Args:
            scoreboard (ScoreboardState): The scoreboard state.
            index (int): The index of the player who made a miss.

        Returns:
            ScoreboardState: The updated scoreboard state with the miss.

        """
        new_scoreboard = type(self).add_misses(scoreboard, index)
        if new_scoreboard[index].misses >= self.lose_threshold:
            new_scoreboard[index].state = PlayerState.LOSE
        new_scoreboard.question_count += 1
        return new_scoreboard

    def through(self, scoreboard: ScoreboardState) -> ScoreboardState:
        """Perform the through operation on the scoreboard.

        Args:
            scoreboard (ScoreboardState): The scoreboard state.

        Returns:
            ScoreboardState: The updated scoreboard state with the through operation.

        """
        new_scoreboard = scoreboard.copy()
        new_scoreboard.question_count += 1
        return new_scoreboard

    def __call__(
        self, scoreboard: ScoreboardState, payload: Payload
    ) -> ScoreboardState:
        """Update the scoreboard state.

        Args:
            scoreboard (ScoreboardState): The scoreboard state.
            payload (int | None): The payload containing the operation type and index.

        Returns:
            ScoreboardState: The updated scoreboard state.

        """
        return super().__call__(scoreboard, payload)

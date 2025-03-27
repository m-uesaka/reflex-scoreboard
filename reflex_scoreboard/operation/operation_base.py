from abc import ABC, abstractmethod

from reflex_scoreboard.data_structure.payload import Payload, PayloadType
from reflex_scoreboard.data_structure.scoreboard import ScoreboardState


class OperationBase(ABC):
    """Base class for scoreboard operations.

    This class provides static methods to manipulate the scoreboard state.
    """

    @abstractmethod
    def through(self, scoreboard: ScoreboardState) -> ScoreboardState:
        """Update the scoreboard by passing the question.

        This method should be implemented by subclasses.

        Args:
            scoreboard (ScoreboardState): The scoreboard state.
            index (int): The index of the player who passed the question.

        Returns:
            ScoreboardState: The updated scoreboard state with the passed question.

        """

    @abstractmethod
    def answer_right(self, scoreboard: ScoreboardState, index: int) -> ScoreboardState:
        """Update the scoreboard by correct answers.

        This method should be implemented by subclasses.

        Args:
            scoreboard (ScoreboardState): The scoreboard state.
            index (int): The index of the player who answered correctly.

        Returns:
            ScoreboardState: The updated scoreboard state with the correct answer.

        """

    @abstractmethod
    def make_miss(self, scoreboard: ScoreboardState, index: int) -> ScoreboardState:
        """Update scoreboard by incorrect answers.

        This method should be implemented by subclasses.

        Args:
            scoreboard (ScoreboardState): The scoreboard state.
            index (int): The index of the player who answered incorrectly.

        Returns:
            ScoreboardState: The updated scoreboard state with the incorrect answer.

        """

    def __call__(
        self, scoreboard: ScoreboardState, payload: Payload
    ) -> ScoreboardState:
        """Update the scoreboard state.

        This method should be implemented by subclasses.

        Args:
            scoreboard (ScoreboardState): The scoreboard state.
            payload (Payload): The payload containing the operation type and index.

        Returns:
            ScoreboardState: The updated scoreboard state.

        """
        if payload.payload_type == PayloadType.RIGHT:
            return self.answer_right(scoreboard, payload.index)
        if payload.payload_type == PayloadType.MISS:
            return self.make_miss(scoreboard, payload.index)
        if payload.payload_type == PayloadType.THROUGH:
            return self.through(scoreboard)

        return scoreboard

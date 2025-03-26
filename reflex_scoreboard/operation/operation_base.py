from abc import ABC, abstractmethod

from reflex_scoreboard.data_structure.payload import Payload, PayloadType
from reflex_scoreboard.data_structure.scoreboard import ScoreboardState


class OperationBase(ABC):
    """Base class for scoreboard operations.

    This class provides static methods to manipulate the scoreboard state.
    """

    @staticmethod
    def reduce_breaks(scoreboard: ScoreboardState) -> ScoreboardState:
        """Reduce the breaks of all players in the scoreboard by 1.

        Args:
            scoreboard (ScoreboardState): The scoreboard state.

        Returns:
            ScoreboardState: The updated scoreboard state with reduced breaks.

        """
        new_scoreboard = scoreboard.copy()
        for player in new_scoreboard.players:
            player.breaks = max(0, player.breaks - 1)
        return new_scoreboard

    @staticmethod
    def add_answers(scoreboard: ScoreboardState, index: int) -> ScoreboardState:
        """Add answers to the player at the given index in the scoreboard.

        Args:
            scoreboard (ScoreboardState): The scoreboard state.
            index (int): The index of the player to add answers to.

        Returns:
            ScoreboardState: The updated scoreboard state with added answers.

        """
        new_scoreboard = scoreboard.copy()
        new_scoreboard[index].answers += 1
        return new_scoreboard

    @staticmethod
    def add_misses(scoreboard: ScoreboardState, index: int) -> ScoreboardState:
        """Add misses to the player at the given index in the scoreboard.

        Args:
            scoreboard (ScoreboardState): The scoreboard state.
            index (int): The index of the player to add misses to.

        Returns:
            ScoreboardState: The updated scoreboard state with added misses.

        """
        new_scoreboard = scoreboard.copy()
        new_scoreboard[index].misses += 1
        return new_scoreboard

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

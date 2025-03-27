from reflex_scoreboard.data_structure.payload import Payload
from reflex_scoreboard.data_structure.scoreboard import ScoreboardState
from reflex_scoreboard.operation.operation_base import OperationBase


class ScoreManager:
    """Class for common manager of scoreboard operations.

    Attributes:
        scoreboard (ScoreboardState): The current state of the scoreboard.
        operation (OperationBase): The operation to perform on the scoreboard.
        undo_stack (list[ScoreboardState]): Stack for undo operations.
        redo_stack (list[ScoreboardState]): Stack for redo operations.

    """

    def __init__(self, scoreboard: ScoreboardState, operation: OperationBase) -> None:
        """Initialize the ScoreManager with a scoreboard state.

        Args:
            scoreboard (ScoreboardState): The initial scoreboard state.
            operation (OperationBase): The operation to perform on the scoreboard.

        """
        self.scoreboard = scoreboard
        self.operation = operation
        self.undo_stack: list[ScoreboardState] = []
        self.redo_stack: list[ScoreboardState] = []

    def stack_to_undo(self) -> None:
        """Add the current state to the undo stack."""
        self.undo_stack.append(self.scoreboard)

    def stack_to_redo(self) -> None:
        """Add the current state to the redo stack."""
        self.redo_stack.append(self.scoreboard)

    def undo(self) -> None:
        """Undo the last operation."""
        if self.undo_stack:
            self.stack_to_redo()
            self.scoreboard = self.undo_stack.pop()

    def redo(self) -> None:
        """Redo the last undone operation."""
        if self.redo_stack:
            self.stack_to_undo()
            self.scoreboard = self.redo_stack.pop()

    def __call__(self, payload: Payload) -> None:
        """Perform the operation on the scoreboard.

        Args:
            payload (Payload): The payload containing the operation details.

        """
        self.stack_to_undo()
        self.scoreboard = self.operation(self.scoreboard, payload)

import dataclasses

import pytest

from reflex_scoreboard.data_structure.player import PlayerScore, PlayerState
from reflex_scoreboard.data_structure.scoreboard import ScoreboardState
from reflex_scoreboard.operation.nomx import NoMxOperation


@pytest.fixture
def prepare_scoreboard_state() -> ScoreboardState:
    """Fixture to create a mock scoreboard state."""
    return ScoreboardState(
        [
            PlayerScore(
                player_id=1, name="Alice", answers=0, misses=0, score=0, breaks=0
            ),
            PlayerScore(
                player_id=2, name="Bob", answers=0, misses=0, score=0, breaks=0
            ),
        ]
    )


class TestNoMxOperation:
    @staticmethod
    def test_answer_right(prepare_scoreboard_state: ScoreboardState) -> None:
        """Test that answer_right increments the player's answers."""
        operation = NoMxOperation(win_threshold=3, lose_threshold=3)
        updated_scoreboard = operation.answer_right(prepare_scoreboard_state, index=0)

        assert updated_scoreboard[0].answers == 1
        assert updated_scoreboard[0].state == PlayerState.NORMAL
        assert updated_scoreboard[0].misses == 0

        assert updated_scoreboard[1].answers == 0
        assert updated_scoreboard[1].state == PlayerState.NORMAL
        assert updated_scoreboard[1].misses == 0

    @staticmethod
    def test_answer_right_with_win(prepare_scoreboard_state: ScoreboardState) -> None:
        current_scoreboard = dataclasses.replace(prepare_scoreboard_state)
        current_scoreboard[0].answers = 4
        operation = NoMxOperation(win_threshold=5, lose_threshold=2)
        updated_scoreboard = operation.answer_right(current_scoreboard, index=0)

        assert updated_scoreboard[0].answers == 5
        assert updated_scoreboard[0].state == PlayerState.WIN

    @staticmethod
    def test_make_miss(prepare_scoreboard_state: ScoreboardState) -> None:
        """Test that make_miss increments the player's misses."""
        operation = NoMxOperation(win_threshold=3, lose_threshold=3)
        updated_scoreboard = operation.make_miss(prepare_scoreboard_state, index=0)

        assert updated_scoreboard[0].misses == 1
        assert updated_scoreboard[0].state is PlayerState.NORMAL
        assert updated_scoreboard[0].answers == 0

        assert updated_scoreboard[1].misses == 0
        assert updated_scoreboard[1].state is PlayerState.NORMAL
        assert updated_scoreboard[1].answers == 0

    @staticmethod
    def test_make_miss_with_lose(prepare_scoreboard_state: ScoreboardState) -> None:
        current_scoreboard = dataclasses.replace(prepare_scoreboard_state)
        current_scoreboard[0].misses = 1
        operation = NoMxOperation(win_threshold=5, lose_threshold=2)
        updated_scoreboard = operation.make_miss(current_scoreboard, index=0)

        assert updated_scoreboard[0].misses == 2
        assert updated_scoreboard[0].state == PlayerState.LOSE
        assert updated_scoreboard[0].answers == 0

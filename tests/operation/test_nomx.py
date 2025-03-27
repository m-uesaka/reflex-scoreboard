import dataclasses

import pytest

from reflex_scoreboard.data_structure.payload import Payload, PayloadType
from reflex_scoreboard.data_structure.player import PlayerScore, PlayerState
from reflex_scoreboard.data_structure.scoreboard import ScoreboardState
from reflex_scoreboard.operation.nomx import NoMxOperation


@pytest.fixture
def prepare_scoreboard_state() -> ScoreboardState:
    """Fixture to create a mock scoreboard state."""
    player1 = PlayerScore(player_id=1, name="Alice")
    player2 = PlayerScore(player_id=2, name="Bob")
    return ScoreboardState(players=[player1, player2], question_count=1)


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
        current_scoreboard = prepare_scoreboard_state.replace_player(
            1, dataclasses.replace(prepare_scoreboard_state[1], answers=4)
        ).set_question_count(20)
        operation = NoMxOperation(win_threshold=5, lose_threshold=2)
        updated_scoreboard = operation.answer_right(current_scoreboard, index=1)

        assert updated_scoreboard.question_count == 21
        assert updated_scoreboard[1].answers == 5
        assert updated_scoreboard[1].state == PlayerState.WIN

    @staticmethod
    def test_make_miss(prepare_scoreboard_state: ScoreboardState) -> None:
        """Test that make_miss increments the player's misses."""
        operation = NoMxOperation(win_threshold=3, lose_threshold=3)
        updated_scoreboard = operation.make_miss(prepare_scoreboard_state, index=0)

        assert updated_scoreboard.question_count == 2
        assert updated_scoreboard[0].misses == 1
        assert updated_scoreboard[0].state is PlayerState.NORMAL
        assert updated_scoreboard[0].answers == 0

        assert updated_scoreboard[1].misses == 0
        assert updated_scoreboard[1].state is PlayerState.NORMAL
        assert updated_scoreboard[1].answers == 0

    @staticmethod
    def test_make_miss_with_lose(prepare_scoreboard_state: ScoreboardState) -> None:
        current_scoreboard = prepare_scoreboard_state.replace_player(
            0, dataclasses.replace(prepare_scoreboard_state[0], misses=1)
        ).set_question_count(20)
        operation = NoMxOperation(win_threshold=5, lose_threshold=2)
        updated_scoreboard = operation.make_miss(current_scoreboard, index=0)

        assert updated_scoreboard.question_count == 21
        assert updated_scoreboard[0].misses == 2
        assert updated_scoreboard[0].state == PlayerState.LOSE
        assert updated_scoreboard[0].answers == 0

    @staticmethod
    def test_through(prepare_scoreboard_state: ScoreboardState) -> None:
        """Test that through increments the question count."""
        operation = NoMxOperation(win_threshold=3, lose_threshold=3)
        updated_scoreboard = operation.through(prepare_scoreboard_state)

        assert updated_scoreboard.question_count == 2
        assert updated_scoreboard[0].answers == 0
        assert updated_scoreboard[0].misses == 0
        assert updated_scoreboard[0].state == PlayerState.NORMAL
        assert updated_scoreboard[1].answers == 0
        assert updated_scoreboard[1].misses == 0
        assert updated_scoreboard[1].state == PlayerState.NORMAL

    @staticmethod
    @pytest.mark.parametrize(
        (
            "payload",
            "expected_answers_list",
            "expected_misses_list",
            "expected_states_list",
        ),
        [
            (
                Payload(PayloadType.RIGHT, extended_index=0),
                [5, 2],
                [0, 1],
                [PlayerState.WIN, PlayerState.NORMAL],
            ),
            (
                Payload(PayloadType.MISS, extended_index=1),
                [4, 2],
                [0, 2],
                [PlayerState.NORMAL, PlayerState.LOSE],
            ),
            (
                Payload(PayloadType.THROUGH),
                [4, 2],
                [0, 1],
                [PlayerState.NORMAL, PlayerState.NORMAL],
            ),
        ],
    )
    def test_call(
        prepare_scoreboard_state: ScoreboardState,
        payload: Payload,
        expected_answers_list: list[int],
        expected_misses_list: list[int],
        expected_states_list: list[PlayerState],
    ) -> None:
        """Test that the call method updates the scoreboard based on the payload."""
        current_scoreboard = (
            prepare_scoreboard_state.replace_player(
                0, dataclasses.replace(prepare_scoreboard_state[0], answers=4)
            )
            .replace_player(
                1, dataclasses.replace(prepare_scoreboard_state[1], answers=2, misses=1)
            )
            .set_question_count(20)
        )
        operation = NoMxOperation(win_threshold=5, lose_threshold=2)
        updated_scoreboard = operation(current_scoreboard, payload)

        assert updated_scoreboard.question_count == 21
        for i in range(len(updated_scoreboard)):
            assert updated_scoreboard[i].answers == expected_answers_list[i]
            assert updated_scoreboard[i].misses == expected_misses_list[i]
            assert updated_scoreboard[i].state == expected_states_list[i]

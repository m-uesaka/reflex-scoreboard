import pytest

from reflex_scoreboard.data_structure.payload import Payload, PayloadType
from reflex_scoreboard.data_structure.player import PlayerScore
from reflex_scoreboard.data_structure.scoreboard import ScoreboardState
from reflex_scoreboard.manager.score_manager import ScoreManager
from reflex_scoreboard.operation.nomx import NoMxOperation


@pytest.fixture
def prepare_score_manager() -> ScoreManager:
    initial_scoreboard = ScoreboardState(
        players=[
            PlayerScore(player_id=1, name="Alice"),
            PlayerScore(player_id=2, name="Bob"),
        ],
        question_count=1,
    )
    operation = NoMxOperation(win_threshold=5, lose_threshold=2)
    return ScoreManager(initial_scoreboard, operation)


class TestScoreManager:
    @staticmethod
    def test_redo_undo_are_empty(prepare_score_manager: ScoreManager) -> None:
        assert not prepare_score_manager.undo_stack
        assert not prepare_score_manager.redo_stack

    @staticmethod
    def test_stack_to_undo(prepare_score_manager: ScoreManager) -> None:
        prepare_score_manager.stack_to_undo()
        assert prepare_score_manager.undo_stack == [prepare_score_manager.scoreboard]
        assert not prepare_score_manager.redo_stack

    @staticmethod
    def test_stack_to_redo(prepare_score_manager: ScoreManager) -> None:
        prepare_score_manager.stack_to_redo()
        assert prepare_score_manager.redo_stack == [prepare_score_manager.scoreboard]
        assert not prepare_score_manager.undo_stack

    @staticmethod
    def test_call(prepare_score_manager: ScoreManager) -> None:
        current_scoreboard = prepare_score_manager.scoreboard
        prepare_score_manager(Payload(PayloadType.RIGHT, extended_index=0))
        assert prepare_score_manager.scoreboard[0].answers == 1
        assert len(prepare_score_manager.undo_stack) == 1
        assert prepare_score_manager.undo_stack[0] == current_scoreboard

    @staticmethod
    def test_undo(prepare_score_manager: ScoreManager) -> None:
        scoreboard_history_list = [prepare_score_manager.scoreboard]
        prepare_score_manager(Payload(PayloadType.RIGHT, extended_index=0))
        scoreboard_history_list.append(prepare_score_manager.scoreboard)
        prepare_score_manager(Payload(PayloadType.MISS, extended_index=1))
        scoreboard_history_list.append(prepare_score_manager.scoreboard)
        assert len(prepare_score_manager.undo_stack) == 2
        prepare_score_manager.undo()
        assert prepare_score_manager.scoreboard == scoreboard_history_list[1]
        assert prepare_score_manager.undo_stack == [scoreboard_history_list[0]]
        assert prepare_score_manager.redo_stack == [scoreboard_history_list[2]]

        prepare_score_manager.undo()
        assert prepare_score_manager.scoreboard == scoreboard_history_list[0]
        assert not prepare_score_manager.undo_stack
        assert prepare_score_manager.redo_stack == [
            scoreboard_history_list[2],
            scoreboard_history_list[1],
        ]

        prepare_score_manager.undo()
        assert prepare_score_manager.scoreboard == scoreboard_history_list[0]
        assert not prepare_score_manager.undo_stack
        assert prepare_score_manager.redo_stack == [
            scoreboard_history_list[2],
            scoreboard_history_list[1],
        ]

    @staticmethod
    def test_redo(prepare_score_manager: ScoreManager) -> None:
        scoreboard_history_list = [prepare_score_manager.scoreboard]
        prepare_score_manager(Payload(PayloadType.RIGHT, extended_index=0))
        scoreboard_history_list.append(prepare_score_manager.scoreboard)
        prepare_score_manager(Payload(PayloadType.MISS, extended_index=1))
        scoreboard_history_list.append(prepare_score_manager.scoreboard)
        assert len(prepare_score_manager.undo_stack) == 2
        prepare_score_manager.undo()
        prepare_score_manager.undo()
        prepare_score_manager.redo()
        assert prepare_score_manager.scoreboard == scoreboard_history_list[1]
        assert prepare_score_manager.undo_stack == [scoreboard_history_list[0]]
        assert prepare_score_manager.redo_stack == [scoreboard_history_list[2]]

        prepare_score_manager.redo()
        assert prepare_score_manager.scoreboard == scoreboard_history_list[2]
        assert prepare_score_manager.undo_stack == scoreboard_history_list[:2]
        assert not prepare_score_manager.redo_stack

        prepare_score_manager.redo()
        assert prepare_score_manager.scoreboard == scoreboard_history_list[2]
        assert prepare_score_manager.undo_stack == scoreboard_history_list[:2]
        assert not prepare_score_manager.redo_stack

import pytest

from reflex_scoreboard.data_structure.player import PlayerScore
from reflex_scoreboard.data_structure.scoreboard import ScoreboardState


@pytest.fixture
def prepare_scoreboard_state() -> ScoreboardState:
    return ScoreboardState(
        players=[
            PlayerScore(player_id=1, name="Alice"),
            PlayerScore(player_id=2, name="Bob"),
        ]
    )


class TestScoreboardState:
    @staticmethod
    def test_normal() -> None:
        player1 = PlayerScore(player_id=1, name="Alice")
        player2 = PlayerScore(player_id=2, name="Bob")
        scoreboard = ScoreboardState([player1, player2])

        assert len(scoreboard.players) == 2
        assert scoreboard.players[0] == player1
        assert scoreboard.players[1] == player2
        assert scoreboard.question_count == 1

    @staticmethod
    def test_add_players_normal(prepare_scoreboard_state: ScoreboardState) -> None:
        player3 = PlayerScore(player_id=3, name="Charlie")
        player4 = PlayerScore(player_id=4, name="David")
        new_scoreboard = prepare_scoreboard_state.add_players([player3, player4])
        assert len(new_scoreboard.players) == 4
        assert new_scoreboard.players[2] == player3
        assert new_scoreboard.players[3] == player4
        assert new_scoreboard.question_count == 1

    @staticmethod
    def test_duplicate_players(prepare_scoreboard_state: ScoreboardState) -> None:
        player3 = PlayerScore(player_id=1, name="Alice")
        with pytest.raises(ValueError, match="Players must be different."):
            _ = prepare_scoreboard_state.add_players([player3])

    @staticmethod
    def test_invalid_question_count() -> None:
        with pytest.raises(ValueError, match="Question count must be at least 1."):
            _ = ScoreboardState([], question_count=0)

    @staticmethod
    def test_getitem(prepare_scoreboard_state: ScoreboardState) -> None:
        assert prepare_scoreboard_state[0].player_id == 1
        assert prepare_scoreboard_state[1].player_id == 2
        assert prepare_scoreboard_state[0].name == "Alice"
        assert prepare_scoreboard_state[1].name == "Bob"

    @staticmethod
    def test_get_item_out_of_range(prepare_scoreboard_state: ScoreboardState) -> None:
        with pytest.raises(IndexError, match="Index out of range."):
            _ = prepare_scoreboard_state[2]

    @staticmethod
    def test_create_from_players_dict() -> None:
        players_dict = {1: "Alice", 2: "Bob"}
        scoreboard = ScoreboardState.create_from_players_dict(players_dict)

        assert len(scoreboard.players) == 2
        assert scoreboard.players[0].player_id == 1
        assert scoreboard.players[0].name == "Alice"
        assert scoreboard.players[1].player_id == 2
        assert scoreboard.players[1].name == "Bob"

    @staticmethod
    def test_len(prepare_scoreboard_state: ScoreboardState) -> None:
        assert len(prepare_scoreboard_state) == 2

    @staticmethod
    def test_replace_player(prepare_scoreboard_state: ScoreboardState) -> None:
        new_player = PlayerScore(player_id=3, name="Charlie")
        updated_scoreboard = prepare_scoreboard_state.replace_player(0, new_player)

        assert updated_scoreboard[0].player_id == 3
        assert updated_scoreboard[0].name == "Charlie"
        assert updated_scoreboard[1].player_id == 2
        assert updated_scoreboard[1].name == "Bob"

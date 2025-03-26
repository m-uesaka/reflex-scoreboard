import pytest

from reflex_scoreboard.data_structure.player import PlayerScore
from reflex_scoreboard.data_structure.scoreboard import ScoreboardState


class TestScoreboardState:
    @staticmethod
    def test_add_players_normal() -> None:
        player1 = PlayerScore(player_id=1, name="Alice")
        player2 = PlayerScore(player_id=2, name="Bob")
        scoreboard = ScoreboardState()
        scoreboard.add_players([player1, player2])

        assert len(scoreboard.players) == 2
        assert scoreboard.players[0] == player1
        assert scoreboard.players[1] == player2
        assert scoreboard.question_count == 1

    @staticmethod
    def test_duplicate_players() -> None:
        player1 = PlayerScore(player_id=1, name="Alice")
        player2 = PlayerScore(player_id=1, name="Alice")  # Duplicate player
        scoreboard = ScoreboardState()
        with pytest.raises(ValueError, match="Players must be different."):
            scoreboard.add_players([player1, player2])

    @staticmethod
    def test_invalid_question_count() -> None:
        with pytest.raises(ValueError, match="Question count must be at least 1."):
            _ = ScoreboardState(question_count=0)

    @staticmethod
    def test_get_item() -> None:
        player1 = PlayerScore(player_id=1, name="Alice")
        player2 = PlayerScore(player_id=2, name="Bob")
        scoreboard = ScoreboardState(question_count=5)
        scoreboard.add_players([player1, player2])

        assert scoreboard[0] == player1
        assert scoreboard[1] == player2

    @staticmethod
    def test_get_item_out_of_range() -> None:
        player1 = PlayerScore(player_id=1, name="Alice")
        player2 = PlayerScore(player_id=2, name="Bob")

        scoreboard = ScoreboardState(question_count=5)
        scoreboard.add_players([player1, player2])

        with pytest.raises(IndexError, match="Index out of range."):
            _ = scoreboard[2]

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
    def test_len() -> None:
        player1 = PlayerScore(player_id=1, name="Alice")
        player2 = PlayerScore(player_id=2, name="Bob")
        scoreboard = ScoreboardState(question_count=5)
        scoreboard.add_players([player1, player2])

        assert len(scoreboard) == 2

    @staticmethod
    def test_copy() -> None:
        player1 = PlayerScore(player_id=1, name="Alice")
        player2 = PlayerScore(player_id=2, name="Bob")
        scoreboard = ScoreboardState(question_count=5)
        scoreboard.add_players([player1, player2])

        copied_scoreboard = scoreboard.copy()

        assert len(copied_scoreboard) == len(scoreboard)
        for copy_player, original_player in zip(
            copied_scoreboard.players, scoreboard.players
        ):
            assert copy_player == original_player
            assert copy_player.answers == original_player.answers
            assert copy_player.misses == original_player.misses
            assert copy_player.score == original_player.score
            assert copy_player.breaks == original_player.breaks
            assert copy_player.state == original_player.state
        assert copied_scoreboard.question_count == scoreboard.question_count

import pytest

from reflex_scoreboard.data_structure.player import PlayerScore
from reflex_scoreboard.data_structure.scoreboard import ScoreboardState


class TestScoreboardState:
    @staticmethod
    def test_normal() -> None:
        player1 = PlayerScore(player_id=1, name="Alice")
        player2 = PlayerScore(player_id=2, name="Bob")
        scoreboard = ScoreboardState(players=[player1, player2], question_count=5)

        assert len(scoreboard.players) == 2
        assert scoreboard.players[0] == player1
        assert scoreboard.players[1] == player2
        assert scoreboard.question_count == 5

    @staticmethod
    def test_duplicate_players() -> None:
        player1 = PlayerScore(player_id=1, name="Alice")
        player2 = PlayerScore(player_id=1, name="Alice")  # Duplicate player

        with pytest.raises(ValueError, match="Players must be different."):
            ScoreboardState(players=[player1, player2])

    @staticmethod
    def test_invalid_question_count() -> None:
        player1 = PlayerScore(player_id=1, name="Alice")
        player2 = PlayerScore(player_id=2, name="Bob")

        with pytest.raises(ValueError, match="Question count must be at least 1."):
            ScoreboardState(players=[player1, player2], question_count=0)

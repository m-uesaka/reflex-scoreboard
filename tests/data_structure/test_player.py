import pytest

from reflex_scoreboard.data_structure.player import PlayerScore, PlayerState


class TestPlayerScore:
    @staticmethod
    def test_normal() -> None:
        player = PlayerScore(
            player_id=1,
            name="Alice",
            answers=5,
            misses=1,
            score=10,
            breaks=1,
            state=PlayerState.WIN,
        )
        assert player.player_id == 1
        assert player.name == "Alice"
        assert player.answers == 5
        assert player.misses == 1
        assert player.score == 10
        assert player.breaks == 1
        assert player.state == PlayerState.WIN

        # Check that the dataclass is immutable
        with pytest.raises(AttributeError):
            player.player_id = 2  # type: ignore[misc]

    @staticmethod
    def test_is_same_player() -> None:
        player1 = PlayerScore(player_id=1, name="Alice")
        player2 = PlayerScore(player_id=1, name="Alice")
        player3 = PlayerScore(player_id=2, name="Bob")

        assert player1.is_same_player(player2) is True
        assert player1.is_same_player(player3) is False

    @staticmethod
    def test_defaults() -> None:
        player = PlayerScore(player_id=1, name="Alice")

        assert player.answers == 0
        assert player.misses == 0
        assert player.score == 0
        assert player.breaks == 0
        assert player.state == PlayerState.NORMAL

    @staticmethod
    def test_add_answer() -> None:
        player = PlayerScore(player_id=1, name="Alice")
        updated_player = player.add_answer()

        assert updated_player.answers == 1
        assert updated_player.misses == 0
        assert updated_player.score == 0
        assert updated_player.breaks == 0
        assert updated_player.state == PlayerState.NORMAL

    @staticmethod
    def test_add_miss() -> None:
        player = PlayerScore(player_id=1, name="Alice")
        updated_player = player.add_miss()

        assert updated_player.answers == 0
        assert updated_player.misses == 1
        assert updated_player.score == 0
        assert updated_player.breaks == 0
        assert updated_player.state == PlayerState.NORMAL

    @staticmethod
    def test_update_score() -> None:
        player = PlayerScore(player_id=1, name="Alice")
        updated_player = player.update_score(10)

        assert updated_player.answers == 0
        assert updated_player.misses == 0
        assert updated_player.score == 10
        assert updated_player.breaks == 0
        assert updated_player.state == PlayerState.NORMAL

    @staticmethod
    def test_set_breaks() -> None:
        player = PlayerScore(player_id=1, name="Alice")
        updated_player = player.set_breaks(2)

        assert updated_player.answers == 0
        assert updated_player.misses == 0
        assert updated_player.score == 0
        assert updated_player.breaks == 2
        assert updated_player.state == PlayerState.NORMAL

    @staticmethod
    def test_update_state() -> None:
        player = PlayerScore(player_id=1, name="Alice")
        updated_player = player.update_state(PlayerState.WIN)

        assert updated_player.answers == 0
        assert updated_player.misses == 0
        assert updated_player.score == 0
        assert updated_player.breaks == 0
        assert updated_player.state == PlayerState.WIN

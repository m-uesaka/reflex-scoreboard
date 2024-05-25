import pytest

from abc_scoring_api.player.player_info import PlayerInfo
from abc_scoring_api.player.player_score import (
    PlayerScore10by10,
    PlayerScore10UpDown,
    PlayerScoreFreeze10,
    PlayerScoreSwedish10,
    PlayerState,
)


class TestPlayerScore10by10:
    @staticmethod
    def test_init() -> None:
        player_info = PlayerInfo("山田", "太郎", 1)
        player_score = PlayerScore10by10(player_info)
        assert player_score.player_info == player_info
        assert player_score.gain == 0
        assert player_score.loss == 0
        assert player_score.breaks == 0
        assert player_score.state == PlayerState.NORMAL
        assert player_score.point == 0

    @staticmethod
    @pytest.mark.parametrize(
        "rights, expected_state",
        [
            (0, PlayerState.NORMAL),
            (1, PlayerState.NORMAL),
            (10, PlayerState.WIN),
        ],
    )
    def test_answer_right(rights: int, expected_state: PlayerState) -> None:
        player_info = PlayerInfo("山田", "太郎", 1)
        player_score = PlayerScore10by10(player_info)
        for _ in range(rights):
            player_score.answer_right()
        assert player_score.gain == rights
        assert player_score.state == expected_state

    @staticmethod
    @pytest.mark.parametrize(
        "losses, expected_state",
        [
            (0, PlayerState.NORMAL),
            (1, PlayerState.NORMAL),
            (6, PlayerState.LOSE),
        ],
    )
    def test_answer_wrong(losses: int, expected_state: PlayerState) -> None:
        player_info = PlayerInfo("山田", "太郎", 1)
        player_score = PlayerScore10by10(player_info)
        for _ in range(losses):
            player_score.answer_wrong()
        assert player_score.loss == losses
        assert player_score.state == expected_state

    @staticmethod
    @pytest.mark.parametrize(
        "rights, losses, expected_point",
        [
            (0, 0, 0),
            (1, 0, 10),
            (1, 1, 9),
            (10, 0, 100),
            (11, 1, 99),
            (12, 1, 108),
            (5, 6, 20),
        ],
    )
    def test_point(rights: int, losses: int, expected_point: int) -> None:
        player_info = PlayerInfo("山田", "太郎", 1)
        player_score = PlayerScore10by10(player_info)
        for _ in range(rights):
            player_score.answer_right()
        for _ in range(losses):
            player_score.answer_wrong()
        assert player_score.gain == rights
        assert player_score.loss == losses
        assert player_score.point == expected_point


class TestPlayerScore10UpDown:
    @staticmethod
    def test_init() -> None:
        player_info = PlayerInfo("山田", "太郎", 1)
        player_score = PlayerScore10UpDown(player_info)
        assert player_score.player_info == player_info
        assert player_score.gain == 0
        assert player_score.loss == 0
        assert player_score.breaks == 0
        assert player_score.state == PlayerState.NORMAL
        assert player_score.point == 0

    @staticmethod
    @pytest.mark.parametrize(
        "rights, expected_state",
        [
            (1, PlayerState.NORMAL),
            (10, PlayerState.WIN),
        ],
    )
    def test_answer_right_without_miss(
        rights: int, expected_state: PlayerState
    ) -> None:
        player_info = PlayerInfo("山田", "太郎", 1)
        player_score = PlayerScore10UpDown(player_info)
        for _ in range(rights):
            player_score.answer_right()
        assert player_score.gain == rights
        assert player_score.loss == 0
        assert player_score.point == rights
        assert player_score.state == expected_state

    @staticmethod
    @pytest.mark.parametrize(
        "rights, wrong_time, expected_point, expected_state",
        [
            (5, 2, 4, PlayerState.NORMAL),
            (15, 10, 6, PlayerState.NORMAL),
            (16, 7, 10, PlayerState.WIN),
        ],
    )
    def test_answer_right_with_one_miss(
        rights: int, wrong_time: int, expected_point: int, expected_state: PlayerState
    ) -> None:
        player_info = PlayerInfo("山田", "太郎", 1)
        player_score = PlayerScore10UpDown(player_info)
        for index in range(rights + 1):
            if index == wrong_time - 1:
                player_score.answer_wrong()
            else:
                player_score.answer_right()
        assert player_score.gain == rights
        assert player_score.loss == 1
        assert player_score.point == expected_point
        assert player_score.state == expected_state

    @staticmethod
    def test_answer_wrong_with_lose() -> None:
        player_info = PlayerInfo("山田", "太郎", 1)
        player_score = PlayerScore10UpDown(player_info)

        for _ in range(5):
            player_score.answer_right()
        player_score.answer_wrong()
        for _ in range(2):
            player_score.answer_right()
        player_score.answer_wrong()

        assert player_score.gain == 7
        assert player_score.loss == 2
        assert player_score.point == 0
        assert player_score.state == PlayerState.LOSE


class TestPlayerScoreSwedish10:
    @staticmethod
    def test_init() -> None:
        player_info = PlayerInfo("山田", "太郎", 1)
        player_score = PlayerScoreSwedish10(player_info)
        assert player_score.player_info == player_info
        assert player_score.gain == 0
        assert player_score.loss == 0
        assert player_score.breaks == 0
        assert player_score.state == PlayerState.NORMAL
        assert player_score.point == 0

    @staticmethod
    def test_point() -> None:
        player_info = PlayerInfo("山田", "太郎", 1)
        player_score = PlayerScoreSwedish10(player_info)
        for _ in range(5):
            player_score.answer_right()

        assert player_score.gain == 5
        assert player_score.loss == 0
        assert player_score.point == 5

    @staticmethod
    @pytest.mark.parametrize(
        "rights, expected_penalty",
        [
            (0, 1),
            (1, 2),
            (2, 2),
            (3, 3),
            (4, 3),
            (5, 3),
            (6, 4),
            (7, 4),
            (8, 4),
            (9, 4),
        ],
    )
    def test_answer_wrong(rights: int, expected_penalty: int) -> None:
        player_info = PlayerInfo("山田", "太郎", 1)
        player_score = PlayerScoreSwedish10(player_info)
        for _ in range(rights):
            player_score.answer_right()
        for _ in range(1):
            player_score.answer_wrong()
        assert player_score.gain == rights
        assert player_score.loss == 1
        assert player_score.point == expected_penalty

    @staticmethod
    def test_answer_wrong_with_lose() -> None:
        player_info = PlayerInfo("山田", "太郎", 1)
        player_score = PlayerScoreSwedish10(player_info)
        for _ in range(6):
            player_score.answer_right()
        for _ in range(3):
            player_score.answer_wrong()

        assert player_score.gain == 6
        assert player_score.loss == 3
        assert player_score.point == 6
        assert player_score.penalty == 12
        assert player_score.state == PlayerState.LOSE


class TestPlayerScoreFreeze10:
    @staticmethod
    def test_init() -> None:
        player_info = PlayerInfo("山田", "太郎", 1)
        player_score = PlayerScoreFreeze10(player_info)
        assert player_score.player_info == player_info
        assert player_score.gain == 0
        assert player_score.loss == 0
        assert player_score.breaks == 0
        assert player_score.state == PlayerState.NORMAL
        assert player_score.point == 0
        assert player_score.breaks == 0

    @staticmethod
    @pytest.mark.parametrize(
        "rights, expected_point, expected_state",
        [
            (1, 1, PlayerState.NORMAL),
            (10, 10, PlayerState.WIN),
        ],
    )
    def test_answer_right(
        rights: int, expected_point: int, expected_state: PlayerState
    ) -> None:
        player_info = PlayerInfo("山田", "太郎", 1)
        player_score = PlayerScoreFreeze10(player_info)
        for _ in range(rights):
            player_score.answer_right()
        assert player_score.gain == rights
        assert player_score.loss == 0
        assert player_score.point == expected_point
        assert player_score.state == expected_state

    @staticmethod
    @pytest.mark.parametrize(
        "wrong_times, expected_breaks",
        [
            (1, 1),
            (2, 2),
        ],
    )
    def test_answer_wrong(wrong_times: int, expected_breaks: int) -> None:
        player_info = PlayerInfo("山田", "太郎", 1)
        player_score = PlayerScoreFreeze10(player_info)
        for _ in range(wrong_times):
            player_score.answer_wrong()
        assert player_score.gain == 0
        assert player_score.loss == wrong_times
        assert player_score.breaks == expected_breaks

    @staticmethod
    def test_reduce_breaks() -> None:
        player_info = PlayerInfo("山田", "太郎", 1)
        player_score = PlayerScoreFreeze10(player_info)
        player_score.reduce_breaks()
        assert player_score.breaks == 0

        for _ in range(3):
            player_score.answer_wrong()
        player_score.reduce_breaks()
        assert player_score.breaks == 2

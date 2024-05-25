from abc import ABC, abstractmethod
from enum import Enum

from abc_scoring_api.player_info import PlayerInfo


class PlayerState(Enum):
    """The state of the player."""

    NORMAL = 0
    WIN = 1
    LOSE = -1


class PlayerScore(ABC):
    """Abstract class of player score.

    Attributes:
        player_info (PlayerInfo): The player information.
        gain (int): The number of correct answers.
        loss (int): The number of wrong answers.
        breaks (int): The number of breaks.
        state (PlayerState): The state of the player.
    """

    def __init__(self, player_info: PlayerInfo) -> None:
        """Initialize the player score."""
        self.player_info = player_info
        self.gain = 0
        self.loss = 0
        self.breaks = 0
        self.state = PlayerState.NORMAL

    @abstractmethod
    def answer_right(self) -> None:
        """Define the behavior when the player answers right."""
        self.gain += 1

    @abstractmethod
    def answer_wrong(self) -> None:
        """Define the behavior when the player answers wrong."""
        self.loss += 1

    def reduce_breaks(self) -> None:
        """Reduce the breaks."""
        self.breaks -= 1 if self.breaks > 0 else 0


class PlayerScore10by10(PlayerScore):
    """The player score for 10 by 10."""

    @property
    def point(self) -> int:
        """Get the point."""
        return self.gain * (10 - self.loss)

    @point.setter
    def point(self, value: int) -> None:
        raise AttributeError("point is read-only")

    def answer_right(self) -> None:
        """Define the behavior when the player answers right."""
        super().answer_right()
        if self.point >= 100:
            self.state = PlayerState.WIN

    def answer_wrong(self) -> None:
        """Define the behavior when the player answers wrong."""
        super().answer_wrong()
        if self.loss >= 6:
            self.state = PlayerState.LOSE


class PlayerScore10UpDown(PlayerScore):
    """The player score for 10 up down."""

    def __init__(self, player_info: PlayerInfo) -> None:
        """Initialize the player score for 10 up down."""
        super().__init__(player_info)
        self.point = 0

    def answer_right(self) -> None:
        """Define the behavior when the player answers right."""
        super().answer_right()
        self.point += 1
        if self.point >= 10:
            self.state = PlayerState.WIN

    def answer_wrong(self) -> None:
        """Define the behavior when the player answers wrong."""
        super().answer_wrong()
        self.point = 0
        if self.loss >= 2:
            self.state = PlayerState.LOSE


class PlayerScoreSwedish10(PlayerScore):
    """The player score for Swedish 10."""

    def __init__(self, player_info: PlayerInfo) -> None:
        """Initialize the player score for Swedish 10."""
        super().__init__(player_info)
        self.penalty = 0

    @property
    def point(self) -> int:
        """Get the point."""
        return self.gain

    @point.setter
    def point(self, value: int) -> None:
        raise AttributeError("point is read-only")

    def answer_right(self) -> None:
        """Define the behavior when the player answers right."""
        super().answer_right()
        if self.point >= 10:
            self.state = PlayerState.WIN

    def answer_wrong(self) -> None:
        """Define the behavior when the player answers wrong."""
        super().answer_wrong()
        if self.point == 0:
            self.penalty += 1
        elif 1 <= self.point <= 2:
            self.penalty += 2
        elif 3 <= self.point <= 5:
            self.penalty += 3
        else:
            self.penalty += 4

        if self.penalty >= 10:
            self.state = PlayerState.LOSE


class PlayerScoreFreeze10(PlayerScore):
    """The player score for Freeze 10."""

    @property
    def point(self) -> int:
        """Get the point."""
        return self.gain

    @point.setter
    def point(self, value: int) -> None:
        raise AttributeError("point is read-only")

    def answer_right(self) -> None:
        """Define the behavior when the player answers right."""
        super().answer_right()
        if self.gain >= 10:
            self.state = PlayerState.WIN

    def answer_wrong(self) -> None:
        """Define the behavior when the player answers wrong."""
        super().answer_wrong()
        self.breaks = self.loss

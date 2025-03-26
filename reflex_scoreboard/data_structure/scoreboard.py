from copy import deepcopy

from reflex_scoreboard.data_structure.player import PlayerScore


class ScoreboardState:
    """The dataclass to store the scoreboard state.

    Attributes:
        players (list[PlayerScore]): List of PlayerScore objects.
        question_count (int): Number of questions. Default to 1.

    """

    def __init__(self, question_count: int = 1) -> None:
        """Initialize the ScoreboardState with players and question count.

        Args:
            question_count (int): Number of questions. Default to 1.

        Raises:
            ValueError: If question_count is less than 1.

        """
        if question_count < 1:
            raise ValueError("Question count must be at least 1.")
        self.players: list[PlayerScore] = []
        self.question_count = question_count

    def add_players(self, players: list[PlayerScore]) -> None:
        """Add players to the scoreboard.

        Args:
            players (list[PlayerScore]): List of PlayerScore objects to add.

        """
        for player in players:
            if any(player.is_same_player(p) for p in self.players):
                raise ValueError("Players must be different.")
            self.players.append(player)

    def __getitem__(self, index: int) -> PlayerScore:
        """Get the player at the given index.

        Args:
            index (int): The index of the player to retrieve.

        Returns:
            PlayerScore: The player at the given index.

        """
        if index < 0 or index >= len(self.players):
            raise IndexError("Index out of range.")
        return self.players[index]

    def __len__(self) -> int:
        """Get the number of players in the scoreboard.

        Returns:
            int: The number of players in the scoreboard.

        """
        return len(self.players)

    @staticmethod
    def create_from_players_dict(
        players_dict: dict[int, str],
    ) -> "ScoreboardState":
        """Create a ScoreboardState from a dictionary of players.

        Args:
            players_dict (dict[int, str]): Dictionary of players.
                The keys are player IDs and the values are player names.

        Returns:
            ScoreboardState: The created ScoreboardState object.

        """
        player_score_list = [
            PlayerScore(player_id, name) for player_id, name in players_dict.items()
        ]
        scoreboard = ScoreboardState()
        scoreboard.add_players(player_score_list)
        return scoreboard

    def copy(self) -> "ScoreboardState":
        """Create a copy of the ScoreboardState.

        Returns:
            ScoreboardState: A copy of the ScoreboardState object.

        """
        return deepcopy(self)

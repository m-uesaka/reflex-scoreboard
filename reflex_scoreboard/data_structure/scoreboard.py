import dataclasses

from reflex_scoreboard.data_structure.player import PlayerScore, PlayerState


@dataclasses.dataclass(frozen=True)
class ScoreboardState:
    """The dataclass to store the scoreboard state.

    Attributes:
        players (list[PlayerScore]): List of PlayerScore objects.
        question_count (int): Number of questions. Default to 1.

    """

    players: list[PlayerScore]
    question_count: int = 1

    def __post_init__(self) -> None:
        """Post-initialization to ensure players is a list.

        Raises:
            ValueError: If question_count is less than 1.

        """
        if self.question_count < 1:
            raise ValueError("Question count must be at least 1.")

    def add_players(self, new_players: list[PlayerScore]) -> "ScoreboardState":
        """Add players to the scoreboard.

        Args:
            new_players (list[PlayerScore]): List of PlayerScore objects to add.

        Raises:
            ValueError: If any player is the same as an existing player.

        Returns:
            ScoreboardState: The updated scoreboard state with the added players.

        """
        current_players = self.players
        for new_player in new_players:
            if any(new_player.is_same_player(p) for p in current_players):
                raise ValueError("Players must be different.")
            current_players.append(new_player)
        return dataclasses.replace(self, players=current_players)

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

    def replace_player(self, index: int, new_player: PlayerScore) -> "ScoreboardState":
        """Replace the player at the given index with a new player.

        Args:
            index (int): The index of the player to replace.
            new_player (PlayerScore): The new player to replace with.

        Returns:
            ScoreboardState: The updated scoreboard state with the replaced player.

        """
        players_list = self.players
        players_list[index] = new_player
        return dataclasses.replace(self, players=players_list)

    def add_answer(self, index: int) -> "ScoreboardState":
        """Add an answer to the player at the given index.

        Args:
            index (int): The index of the player to add an answer to.

        Returns:
            ScoreboardState: The updated scoreboard state with the added answer.

        """
        return self.replace_player(index, self.players[index].add_answer())

    def add_miss(self, index: int) -> "ScoreboardState":
        """Add a miss to the player at the given index.

        Args:
            index (int): The index of the player to add a miss to.

        Returns:
            ScoreboardState: The updated scoreboard state with the added miss.

        """
        return self.replace_player(index, self.players[index].add_miss())

    def update_score(self, index: int, score: int) -> "ScoreboardState":
        """Update the score of the player at the given index.

        Args:
            index (int): The index of the player to update.
            score (int): The new score to set.

        Returns:
            ScoreboardState: The updated scoreboard state with the new score.

        """
        return self.replace_player(index, self.players[index].update_score(score))

    def set_breaks(self, index: int, breaks: int) -> "ScoreboardState":
        """Update the number of breaks for the player at the given index.

        Args:
            index (int): The index of the player to update.
            breaks (int): The new number of breaks to set.

        Returns:
            ScoreboardState: The updated scoreboard state with the new breaks.

        """
        return self.replace_player(index, self.players[index].set_breaks(breaks))

    def update_state(self, index: int, state: PlayerState) -> "ScoreboardState":
        """Update the state of the player at the given index.

        Args:
            index (int): The index of the player to update.
            state (PlayerState): The new state to set.

        Returns:
            ScoreboardState: The updated scoreboard state with the new state.

        """
        return self.replace_player(index, self.players[index].update_state(state))

    def reduce_breaks_all(self) -> "ScoreboardState":
        """Reduce the breaks of all players in the scoreboard by 1.

        Returns:
            ScoreboardState: The updated scoreboard state with reduced breaks.

        """
        players_list = [
            player.set_breaks(max(0, player.breaks - 1)) for player in self.players
        ]
        return dataclasses.replace(self, players=players_list)

    def set_question_count(self, count: int) -> "ScoreboardState":
        """Update the question count of the scoreboard.

        Args:
            count (int): The new question count.

        Returns:
            ScoreboardState: The updated scoreboard state with the new question count.

        """
        return dataclasses.replace(self, question_count=count)

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
        players_list = [
            PlayerScore(player_id, name) for player_id, name in players_dict.items()
        ]
        return ScoreboardState(players=players_list)

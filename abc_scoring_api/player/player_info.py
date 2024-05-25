class PlayerInfo:
    """A class to represent a player's information."""

    def __init__(self, family_name: str, given_name: str, entry_no: int) -> None:
        """Initialize a new player info object.

        Args:
            family_name (str): family name
            given_name (str): given name
            entry_no (int): entry number
        """
        self.family_name = family_name
        self.given_name = given_name
        self.entry_no = entry_no

    @property
    def full_name(self) -> str:
        """Get the full name of the player.

        Returns:
            str: full name
        """
        return f"{self.family_name}　{self.given_name}"

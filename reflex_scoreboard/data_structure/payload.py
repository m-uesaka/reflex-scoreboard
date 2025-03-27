from dataclasses import dataclass
from enum import Enum
from typing import cast


class PayloadType(Enum):
    """Enum for payload types."""

    RIGHT = 1
    THROUGH = 0
    MISS = -1


@dataclass
class Payload:
    """Class for payload.

    Attributes:
        payload_type (PayloadType): Type of the payload.
        index (int | None): Index of the player. Required for RIGHT and MISS payloads.
            Default is None.

    """

    payload_type: PayloadType
    extended_index: int | None = None

    def __post_init__(self) -> None:
        """Validate the payload attributes.

        Raises:
            ValueError: If index is None for RIGHT or MISS payloads.

        """
        if self.payload_type != PayloadType.THROUGH and self.extended_index is None:
            raise ValueError("Index must be provided for RIGHT and MISS payloads.")

    @property
    def index(self) -> int:
        """Get the index of the payload.

        Returns:
            int: Index of the payload.

        """
        if self.payload_type != PayloadType.THROUGH:
            return cast(int, self.extended_index)
        raise ValueError("Index is not available for THROUGH payloads.")

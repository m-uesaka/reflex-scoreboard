import pytest

from reflex_scoreboard.data_structure.payload import Payload, PayloadType


class TestPayload:
    @staticmethod
    @pytest.mark.parametrize(
        ("payload_type", "index"),
        [
            (PayloadType.RIGHT, 1),
            (PayloadType.MISS, 2),
            (PayloadType.THROUGH, None),
            (PayloadType.THROUGH, 0),  # allow int for THROUGH
        ],
    )
    def test_normal(payload_type: PayloadType, index: int | None) -> None:
        payload = Payload(payload_type, extended_index=index)
        assert payload.payload_type == payload_type
        assert payload.extended_index == index

    @staticmethod
    @pytest.mark.parametrize(
        ("payload_type", "index"),
        [
            (PayloadType.RIGHT, None),
            (PayloadType.MISS, None),
        ],
    )
    def test_value_error(payload_type: PayloadType, index: int | None) -> None:
        with pytest.raises(
            ValueError, match="Index must be provided for RIGHT and MISS payloads."
        ):
            Payload(payload_type=payload_type, extended_index=index)

    @staticmethod
    def test_property_index_value_error() -> None:
        payload = Payload(payload_type=PayloadType.THROUGH)
        with pytest.raises(
            ValueError, match="Index is not available for THROUGH payloads."
        ):
            _ = payload.index

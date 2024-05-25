from abc_scoring_api.player_info import PlayerInfo


class TestPlayerInfo:
    def test_full_name(self):
        player = PlayerInfo("山田", "太郎", 1)
        assert player.full_name == "山田　太郎"

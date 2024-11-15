from models import Channel

class ChannelRepository:
    def populate_table(self) -> None:
        raise NotImplementedError  # pragma: no cover

    def get_random_channel(self) -> Channel:
        raise NotImplementedError  # pragma: no cover

    def delete_all_channels(self) -> None:
        raise NotImplementedError  # pragma: no cover
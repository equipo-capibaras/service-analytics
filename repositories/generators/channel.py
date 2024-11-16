import secrets
from uuid import uuid4

from db import db
from models import Channel
from models.enums import ChannelEnum
from repositories import ChannelRepository


class GeneratorChannelRepository(ChannelRepository):
    def __init__(self) -> None:
        self.db = db

    def populate_table(self) -> None:
        channels = []
        channel_1 = Channel(id=str(uuid4()), channel_type=ChannelEnum.EMAIL.value)
        channels.append(channel_1)

        channel_2 = Channel(id=str(uuid4()), channel_type=ChannelEnum.WEB.value)
        channels.append(channel_2)

        channel_3 = Channel(id=str(uuid4()), channel_type=ChannelEnum.MOBILE.value)
        channels.append(channel_3)

        self.db.session.add_all(channels)
        self.db.session.commit()

    def get_random_channel(self) -> Channel:
        channels = self.db.session.query(Channel).all()
        return secrets.choice(channels)

    def delete_all_channels(self) -> None:
        self.db.session.query(Channel).delete()
        self.db.session.commit()

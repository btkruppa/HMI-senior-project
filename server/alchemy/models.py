from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from alchemy.setup import Base
import datetime

class User(Base):
    __tablename__ = 'users'
    wwuid = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    mask_photo = Column(String(250))
    subscriptions = Column(String(2500))
    def to_json(self):
        return {'wwuid': str(self.wwuid), 'name': str(self.name), 'mask_photo': str(self.mask_photo), 'subscriptions': str(self.subscriptions)}

class Feed(Base):
    __tablename__ = 'feeds'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    description = Column(String(250))
    owner = Column(Integer, ForeignKey("users.wwuid"), nullable=False)
    administrators = Column(String(1000))
    private = Column(Boolean, default=True)
    def to_json(self):
        return {'id': str(self.id), 'title': str(self.title), 'description': str(self.description), 'owner': str(self.owner), 'administrators': str(self.administrators), 'private': str(self.private)}

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    feed_id = Column(Integer, ForeignKey("feed.id"), nullable=False)
    left = Column(String(250))
    top = Column(String(250))
    type = Column(String(250))
    border = Column(String(250))
    plc = Column(String(250))
    color = Column(String(250))
    size = Column(String(250))
    level = Column(Integer)
    label = Column(String(250))
    #creator = Column(Integer, ForeignKey("users.wwuid"), nullable=False)
    #updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    def to_json(self):
        return {'id': str(self.id), 'feed_id': str(self.feed_id), 'left': str(self.left), 'top': str(self.top), 'type': str(self.type), 'boarder': str(self.boarder), 'plc': str(self.plc), 'color': str(self.color), 'size': str(self.size), 'level': str(self.level), 'label': str(self.label)}

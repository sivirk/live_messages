# -*- coding: UTF-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


association_table = Table(
    'registers_message_tag', Base.metadata,
    Column('tag_id', Integer, ForeignKey('registers_tag.id')),
    Column('message_id', Integer, ForeignKey('registers_message.id'))
)


class Tag(Base):
    __tablename__ = "registers_tag"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content_type_id = Column(Integer)


class Message(Base):
    __tablename__ = "registers_message"

    id = Column(Integer, primary_key=True)
    text = Column(String,)
    purpose = Column(Integer)
    user_id = Column(Integer)
    register_id = Column(Integer, ForeignKey('registers_register.id'))
    tags = relationship("Tag", secondary=association_table)

    def __unicode__(self,):
        return u"Сообщение: %s" % self.id


class Dairy(Base):
    __tablename__ = "registers_register"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    slug = Column(String)

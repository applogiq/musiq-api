from sqlalchemy import Column, Float, Integer, String
from sqlalchemy_json import NestedMutableJson
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import sqlalchemy

from config.database import engine
from config.database import Base

class admin_users(Base):
    __tablename__ = "admin_users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    is_delete = Column(Integer)
    is_active = Column(Integer)
    

    # recent = relationship("recents", backref="users")
    # last = relationship("last_songs", backref="users")
    # fav = relationship("favourites", backref="users")
    # playlist_song = relationship("playlist", backref="users")


class admin_token(Base):
    __tablename__ = "admin_token"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    refresh_token = Column(String)
    access_token = Column(String)

metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
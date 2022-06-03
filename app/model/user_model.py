from enum import unique
from sqlalchemy import Column, Integer, String, ARRAY,JSON
from sqlalchemy_json import NestedMutableJson
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import sqlalchemy

from app.config.database import SessionLocal, engine
from app.config.database import Base
# from app.model.recent_model import recents
# from app.model.last_song_model import last_songs
# from app.model.favourite_model import favourites



class users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    register_id = Column(Integer,unique=True)
    fullname = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    preference = Column(NestedMutableJson)
    is_image = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    is_delete = Column(Integer)
    is_active = Column(Integer)
    

    recent = relationship("recents", backref="users")
    last = relationship("last_songs", backref="users")
    fav = relationship("favourites", backref="users")


class token(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True, index=True)
    # owner_id = Column(Integer, ForeignKey("users.id"))
    email = Column(String)
    refresh_token = Column(String)
    access_token = Column(String)

    # owner = relationship("User", back_populates="token")

metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
from enum import unique
from sqlalchemy import DATE,Boolean, Column, Integer,TIME, LargeBinary, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import sqlalchemy

from config.database import SessionLocal, engine
from config.database import Base
from model.user_model import users
from model.song_model import songs

class last_songs(Base):
    __tablename__ = "last_song"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.register_id"),nullable=True) 
    song_id = Column(Integer,ForeignKey("songs.id"),nullable=True)
    duration = Column(TIME,nullable=True)
    paused_timing = Column(TIME,nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer,nullable=True)
    created_user_by = Column(Integer,nullable=True)
    updated_by = Column(Integer,nullable=True)
    updated_user_by = Column(Integer,nullable=True)
    is_delete = Column(Boolean,default=False)
    is_active = Column(Boolean,default=True)
    # last = relationship("users")
    # last = relationship("songs")
    # songs = relationship("artist")

metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
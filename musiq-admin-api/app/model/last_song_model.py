from enum import unique
from sqlalchemy import Boolean, Column, Integer,TIME, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import sqlalchemy

from config.database import *
from model.user_model import users
from model.song_model import songs


###table creation for user's last-song detail
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

###code to create all the table in this file
metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
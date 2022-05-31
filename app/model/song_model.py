from enum import unique
from sqlalchemy import   DATE, Column, Integer,TIME, LargeBinary, String, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import sqlalchemy

from app.config.database import SessionLocal, engine
from app.config.database import Base

class songs(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(String(255))
    song_name = Column(String(255), nullable=True) 
    artist_id = Column(JSON, default=dict)
    album_id = Column(String, nullable=True)
    genre_id = Column(JSON, default=dict)
    duration = Column(TIME,nullable=True)
    lyrics = Column(String,nullable=True)  
    listeners = Column(Integer,nullable=True)
    label = Column(String,nullable=True)
    released_date = Column(DATE,nullable=True)
    song_size = Column(String,nullable=True)
    is_music = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    is_delete = Column(Integer)
    is_active = Column(Integer)
    
metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)


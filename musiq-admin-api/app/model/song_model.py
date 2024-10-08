from sqlalchemy import DATE,Column, Integer, String,JSON,ForeignKey,TIME,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy

from config.database import *
from model.album_model import *

###table for song detail
class songs(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(String(255),unique = True)
    song_name = Column(String(255), nullable=True) 
    artist_id = Column(ARRAY(Integer))
    album_id = Column(Integer, ForeignKey("albums.id"))
    genre_id = Column(JSON)
    duration = Column(TIME,nullable=True)
    lyrics = Column(String,nullable=True)  
    listeners = Column(Integer,nullable=True)
    label = Column(String,nullable=True)
    released_date = Column(DATE,nullable=True)
    song_size = Column(String,nullable=True)
    is_music = Column(Boolean,default=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer,nullable=True)
    updated_by = Column(Integer,nullable=True)
    is_delete = Column(Boolean,default=False)
    is_active = Column(Boolean,default=True)


    ###reference for foreign key usage
    last_song = relationship("last_songs",backref="songs")
    fav = relationship("favourites",backref="songs")
    aura = relationship("aura_songs",backref="songs")
    playlist_song = relationship("playlist_songs",backref="songs")


from config.database import *
from sqlalchemy import Column, Integer, String, TIMESTAMP,text,Boolean
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

###table creation for album detail
class albums(Base):
    __tablename__ = "albums"
     
    id = Column(Integer, primary_key=True, index=True)
    album_id = Column(String(255),unique=True,nullable=False)
    album_name = Column(String(255), nullable=False)
    released_year = Column(Integer)
    no_of_songs = Column(Integer) 
    music_director = Column(ARRAY(Integer))
    music_director_name = Column(ARRAY(String))
    is_image = Column(Boolean,default=False)
    premium_status = Column(String,default="free")
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer,nullable=True)
    updated_by = Column(Integer,nullable=True)
    is_delete = Column(Boolean,default=False)
    is_active = Column(Boolean,default=True)

    song = relationship("songs", backref="albums")


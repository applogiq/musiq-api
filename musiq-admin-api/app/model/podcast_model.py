from sqlalchemy import DATE,Column, Float, Integer, String,JSON,ForeignKey,TIME,Boolean
from sqlalchemy_json import NestedMutableJson
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
import sqlalchemy

from config.database import *
from model.podcast_author_model import *
from model.category_model import *

class podcast(Base):
    __tablename__ = "podcast"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=True) 
    description = Column(String(255), nullable=True) 
    no_of_episode = Column(Integer,nullable=True)
    duration = Column(TIME,nullable=True) 
    authors_id = Column(ARRAY(Integer))
    authors_name = Column(ARRAY(String))
    category_id = Column(ARRAY(Integer))
    category_name = Column(ARRAY(String))
    is_image = Column(Boolean,default=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer,nullable=True)
    updated_by = Column(Integer,nullable=True)
    is_delete = Column(Boolean,default=False)
    is_active = Column(Boolean,default=True)

    # song = relationship("albums", backref="songs")

    # last_song = relationship("last_songs",backref="songs")
    # fav = relationship("favourites",backref="songs")
    # aura = relationship("aura_songs",backref="songs")

    # songs = relationship("artist")
    # songs = relationship("genres")

    
metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
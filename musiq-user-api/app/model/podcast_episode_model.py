from sqlalchemy import DATE,Column, Float, Integer, String,JSON,ForeignKey,TIME,Boolean
from sqlalchemy_json import NestedMutableJson
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
import sqlalchemy

from config.database import *
from model.podcast_model import *

###table creation for podcast-episode detail
class podcast_episode(Base):
    __tablename__ = "podcast_episode"
    id = Column(Integer, primary_key=True, index=True)
    podcast_id = Column(Integer, ForeignKey("podcast.id"))
    episode_number = Column(Integer,nullable=True)
    episode_title = Column(String(255), nullable=True) 
    description = Column(String(255), nullable=True) 
    subtitles = Column(String(255), nullable=True)
    duration = Column(TIME,nullable=True) 
    is_audio = Column(Boolean,default=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer,nullable=True)
    updated_by = Column(Integer,nullable=True)
    is_delete = Column(Boolean,default=False)
    is_active = Column(Boolean,default=True)


###code to create all the table in this file      
metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
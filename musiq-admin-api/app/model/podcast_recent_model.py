from enum import unique
from sqlalchemy import DATE, Column, Integer,TIME, LargeBinary, String, JSON,ForeignKey,Boolean
from sqlalchemy_json import NestedMutableJson
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import sqlalchemy

from config.database import SessionLocal, engine
from config.database import Base
from model.user_model import users

class podcast_recents(Base):
    __tablename__ = "podcast_recents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id")) 
    podcast_id = Column(Integer, ForeignKey("podcast.id"))
    episode_id = Column(Integer, ForeignKey("podcast_episode.id"))
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



metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
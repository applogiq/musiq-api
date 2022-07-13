from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy

from config.database import *
from model.podcast_author_model import *
from model.category_model import *

###table creation for song detail
class podcast(Base):
    __tablename__ = "podcast"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=True) 
    description = Column(String(255), nullable=True) 
    no_of_episode = Column(Integer,nullable=True)
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

    ###reference for foreign key usage
    episode = relationship("podcast_episode",backref="podcast")
    history = relationship("podcast_history",backref="podcast")


###code to create all the table in this file
metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
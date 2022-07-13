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

###table creation for recent list
class recents(Base):
    __tablename__ = "recents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.register_id")) 
    song_id = Column(NestedMutableJson)
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
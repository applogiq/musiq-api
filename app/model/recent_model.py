from enum import unique
from sqlalchemy import DATE, Column, Integer,TIME, LargeBinary, String, JSON,ForeignKey
from sqlalchemy_json import NestedMutableJson
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import sqlalchemy

from app.config.database import SessionLocal, engine
from app.config.database import Base
from app.model.user_model import users

class recents(Base):
    __tablename__ = "recents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.register_id")) 
    song_id = Column(NestedMutableJson)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    is_delete = Column(Integer)
    is_active = Column(Integer)

    recents = relationship("users")

metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
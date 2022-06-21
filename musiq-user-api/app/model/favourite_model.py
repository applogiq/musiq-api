from config.database import SessionLocal,engine
from config.database import Base
from sqlalchemy import Boolean,Column, Integer, String, TIMESTAMP,text,ForeignKey
import sqlalchemy

from model.user_model import users
from model.song_model import songs


class favourites(Base):
    __tablename__ = "favourites"
     
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    song_id = Column(Integer,ForeignKey("songs.id"))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    created_by = Column(Integer)
    created_user_by = Column(Integer)
    is_active = Column(Boolean,default=True)


metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
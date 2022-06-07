from app.config.database import SessionLocal, engine
from app.config.database import Base
from sqlalchemy import   DATE, Column, Integer,TIME, LargeBinary, String, JSON,TIMESTAMP,text,ForeignKey
from sqlalchemy.orm import relationship
import sqlalchemy

from app.model.user_model import users
from app.model.song_model import songs

class favourites(Base):
    __tablename__ = "favourites"
     
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    song_id = Column(Integer,ForeignKey("songs.id"))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    created_by = Column(Integer)
    is_active = Column(Integer)

    # last = relationship("users")
    # last = relationship("songs")

metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
from app.config.database import SessionLocal, engine
from app.config.database import Base
from sqlalchemy_json import NestedMutableJson
from sqlalchemy import   DATE, Column, Integer,TIME, LargeBinary, String, JSON,TIMESTAMP,text,ForeignKey
import sqlalchemy
from sqlalchemy.orm import relationship
# from app.model.aura_song_model import aura_songs
from app.model.user_model import users


class playlist(Base):
    __tablename__ = "playlist"
     
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    name = Column(String(255), nullable=False)
    no_of_songs = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    is_delete = Column(Integer)
    is_active = Column(Integer)

    playlist_song = relationship("playlist_songs", backref="playlist")

metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
from config.database import SessionLocal, engine
from config.database import Base
from sqlalchemy import   DATE, Column, Integer,TIME, LargeBinary, String, JSON,TIMESTAMP,text,ForeignKey,Boolean
from sqlalchemy.orm import relationship
import sqlalchemy
from model.playlist_model import playlist
from model.song_model import songs


class playlist_songs(Base):
    __tablename__ = "playlist_songs"
     
    id = Column(Integer, primary_key=True, index=True)
    playlist_id = Column(Integer,ForeignKey("playlist.id"))
    song_id = Column(Integer,ForeignKey("songs.id"))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer)
    created_user_by = Column(Integer)
    updated_by = Column(Integer)
    updated_user_by = Column(Integer)
    is_delete = Column(Boolean,default=False)
    is_active = Column(Boolean,default=True)

    # aura = relationship("aura")
    # aura = relationship("songs")



metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
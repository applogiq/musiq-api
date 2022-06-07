from app.config.database import SessionLocal, engine
from app.config.database import Base
from sqlalchemy import   DATE, Column, Integer,TIME, LargeBinary, String, JSON,TIMESTAMP,text,ForeignKey
from sqlalchemy.orm import relationship
import sqlalchemy
from app.model.playlist_model import playlist
from app.model.song_model import songs


class playlist_songs(Base):
    __tablename__ = "playlist_songs"
     
    id = Column(Integer, primary_key=True, index=True)
    playlist_id = Column(Integer,ForeignKey("playlist.id"))
    song_id = Column(Integer,ForeignKey("songs.id"))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    is_delete = Column(Integer)
    is_active = Column(Integer)

    # aura = relationship("aura")
    # aura = relationship("songs")



metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
from app.config.database import SessionLocal,engine
from app.config.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP,text
import sqlalchemy
from sqlalchemy.orm import relationship
# from app.model.song_model import songs

class albums(Base):
    __tablename__ = "albums"
     
    id = Column(Integer, primary_key=True, index=True)
    album_id = Column(String(255),unique=True,nullable=False)
    name = Column(String(255), nullable=False)
    released_year = Column(Integer)
    no_of_songs = Column(Integer) 
    music_director = Column(String(255))
    is_image = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    is_delete = Column(Integer)
    is_active = Column(Integer)

    song = relationship("songs", backref="albums")


metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
from app.config.database import SessionLocal, engine
from app.config.database import Base
from sqlalchemy import   DATE, Column, Integer,TIME, LargeBinary, String, JSON,TIMESTAMP,text,ForeignKey
from sqlalchemy.orm import relationship
import sqlalchemy

class aura_songs(Base):
    __tablename__ = "aura_songs"
     
    id = Column(Integer, primary_key=True, index=True)
    aura_id = Column(String(255),ForeignKey("aura.aura_id"))
    song_id = Column(String(255),ForeignKey("songs.song_id"))
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
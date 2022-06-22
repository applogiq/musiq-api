from config.database import *
from sqlalchemy import   Boolean,DATE, Column, Integer,TIME, LargeBinary, String, JSON,TIMESTAMP,text,ForeignKey
from sqlalchemy.orm import relationship
import sqlalchemy

class aura_songs(Base):
    __tablename__ = "aura_songs"
     
    id = Column(Integer, primary_key=True, index=True)
    aura_id = Column(Integer,ForeignKey("aura.id"))
    song_id = Column(Integer,ForeignKey("songs.id"))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    created_by = Column(Integer)
    is_delete = Column(Boolean,default=False)
    is_active = Column(Boolean,default=True)

    # aura = relationship("aura")
    # aura = relationship("songs")



metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
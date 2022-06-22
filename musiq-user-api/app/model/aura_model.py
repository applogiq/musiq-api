from config.database import *
from sqlalchemy_json import NestedMutableJson
from sqlalchemy import   DATE, Column, Integer,TIME, LargeBinary, String, JSON,TIMESTAMP,text,Boolean
import sqlalchemy
from sqlalchemy.orm import relationship
# from app.model.aura_song_model import aura_songs


class aura(Base):
    __tablename__ = "aura"
     
    id = Column(Integer, primary_key=True, index=True)
    aura_id = Column(String(255),unique=True,nullable=False)
    aura_name = Column(String(255), nullable=False)
    no_of_songs = Column(Integer)
    is_image = Column(Boolean,default=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    is_delete = Column(Boolean,default=False)
    is_active = Column(Boolean,default=True)


    # aura_song = relationship("aura_songs", backref="aura")

metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
from app.config.database import SessionLocal, engine
from app.config.database import Base
from sqlalchemy_json import NestedMutableJson
from sqlalchemy import   DATE, Column, Integer,TIME, LargeBinary, String, JSON,TIMESTAMP,text
import sqlalchemy
from sqlalchemy.orm import relationship
# from app.model.aura_song_model import aura_songs


class aura(Base):
    __tablename__ = "aura"
     
    id = Column(Integer, primary_key=True, index=True)
    aura_id = Column(String(255),unique=True,nullable=False)
    name = Column(String(255), nullable=False)
    is_image = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    is_delete = Column(Integer)
    is_active = Column(Integer)

    aura_song = relationship("aura_songs", backref="aura")

metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
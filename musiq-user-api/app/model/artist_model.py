from config.database import engine
from config.database import Base
from sqlalchemy import DATE, Column, Integer, String,TIMESTAMP,text,Boolean
import sqlalchemy
from sqlalchemy.orm import relationship
# from app.model.album_model import albums



class artist(Base):
    __tablename__ = "artist"
     
    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(String(255),unique=True,nullable=False)
    name = Column(String(255), nullable=False)
    followers = Column(Integer) 
    is_image = Column(Boolean)
    # img_link = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer,nullable=True)
    updated_by = Column(Integer,nullable=True)
    is_delete = Column(Boolean)
    is_active = Column(Boolean)

    # album = relationship("albums", backref="artist")

metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
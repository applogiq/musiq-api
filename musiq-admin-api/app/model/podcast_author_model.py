from config.database import engine
from config.database import Base
from sqlalchemy import DATE, Column, Integer, String,TIMESTAMP,text,Boolean
import sqlalchemy
from sqlalchemy.orm import relationship
# from app.model.album_model import albums



class podcast_author(Base):
    __tablename__ = "podcast_author"
     
    id = Column(Integer, primary_key=True, index=True)
    author_name = Column(String(255), nullable=False)
    is_image = Column(Boolean,default=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer,nullable=True)
    updated_by = Column(Integer,nullable=True)
    is_delete = Column(Boolean,default=False)
    is_active = Column(Boolean,default=True)

    # album = relationship("albums", backref="artist")

metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
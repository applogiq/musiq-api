from config.database import engine
from config.database import Base
from sqlalchemy import DATE, Column, Integer, String,TIMESTAMP,text,Boolean
import sqlalchemy


###table creation for artist detail
class artist(Base):
    __tablename__ = "artist"
     
    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(String(255),unique=True,nullable=False)
    artist_name = Column(String(255), nullable=False)
    followers = Column(Integer) 
    is_image = Column(Boolean)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer,nullable=True)
    updated_by = Column(Integer,nullable=True)
    is_delete = Column(Boolean)
    is_active = Column(Boolean)

 ###code to create all the table in this file   
metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
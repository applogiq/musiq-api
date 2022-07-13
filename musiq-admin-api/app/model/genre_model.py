from config.database import SessionLocal,engine
from config.database import Base
from sqlalchemy import Boolean,Column, Integer, String, TIMESTAMP,text
import sqlalchemy

###table creation for podcast-history detail
class genres(Base):
    __tablename__ = "genres"
     
    id = Column(Integer, primary_key=True, index=True)
    genre_id = Column(String(255),unique=True,nullable=False)
    genre_name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer,nullable=True)
    updated_by = Column(Integer,nullable=True)
    is_delete = Column(Boolean,default=False)
    is_active = Column(Boolean,default=True)

###code to create all the table in this file
metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)

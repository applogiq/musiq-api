from app.config.database import SessionLocal,engine
from app.config.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP,text
import sqlalchemy

class genres(Base):
    __tablename__ = "genres"
     
    id = Column(Integer, primary_key=True, index=True)
    genre_id = Column(String(255),unique=True,nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    is_delete = Column(Integer)
    is_active = Column(Integer)


metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)

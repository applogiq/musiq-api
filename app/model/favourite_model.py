from app.config.database import SessionLocal, engine
from app.config.database import Base
from sqlalchemy import   DATE, Column, Integer,TIME, LargeBinary, String, JSON,TIMESTAMP,text
import sqlalchemy

class favourites(Base):
    __tablename__ = "favourites"
     
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    song_id = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    created_by = Column(Integer)
    is_active = Column(Integer)

metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
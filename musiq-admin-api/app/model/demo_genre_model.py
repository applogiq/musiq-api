from config.database import SessionLocal,engine
from config.database import Base
from sqlalchemy import Boolean,Column, Integer, String, TIMESTAMP,text,ForeignKey
import sqlalchemy

# from model.user_model import users
# from model.song_model import songs


class demo_genre(Base):
    __tablename__ = "demo_genre"
     
    id = Column(Integer, primary_key=True, index=True)
    genre_name = Column(String)

metadata = sqlalchemy.MetaData()
Base.metadata.create_all(bind=engine)
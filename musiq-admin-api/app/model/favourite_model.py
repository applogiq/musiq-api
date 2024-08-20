from sqlalchemy import Boolean,Column, Integer, TIMESTAMP,text,ForeignKey
import sqlalchemy

from config.database import *
from model.user_model import users
from model.song_model import songs

###table creation for user's favourite detail
class favourites(Base):
    __tablename__ = "favourites"
     
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    song_id = Column(Integer,ForeignKey("songs.id"))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    created_by = Column(Integer)
    created_user_by = Column(Integer)
    is_active = Column(Boolean,default=True)


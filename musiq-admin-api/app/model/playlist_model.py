from config.database import engine
from config.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP,text,ForeignKey,Boolean
import sqlalchemy
from model.user_model import users
from sqlalchemy.orm import relationship


###table creation for user's playlist detail
class playlist(Base):
    __tablename__ = "playlist"
     
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    playlist_name = Column(String(255), nullable=False)
    no_of_songs = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer)
    created_user_by = Column(Integer)
    updated_by = Column(Integer)
    updated_user_by = Column(Integer)
    is_delete = Column(Boolean,default=False)
    is_active = Column(Boolean,default=True)

    ###reference for foreign key usage
    playlist_song = relationship("playlist_songs",backref="playlist")


# from email.policy import default
from sqlalchemy import Boolean, Column, Float, Integer, String
from sqlalchemy_json import NestedMutableJson
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import sqlalchemy

from config.database import *

###create model for user table
class users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    register_id = Column(Integer,unique=True)
    fullname = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    preference = Column(NestedMutableJson)
    is_preference = Column(Boolean,default=False)
    otp = Column(String)
    otp_time = Column(Float)
    is_image = Column(Boolean,default=False)
    premium_status = Column(String,default="free") 
    subscription_end_date = Column(TIMESTAMP(timezone=True),nullable=True) 
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'))
    created_by = Column(Integer,nullable=True)
    created_user_by = Column(Integer,nullable=True)
    updated_by = Column(Integer,nullable=True)
    updated_user_by = Column(Integer,nullable=True)
    is_delete = Column(Boolean,default=False)
    is_active = Column(Boolean,default=True)
    
    ###reference for foreign key usage
    recent = relationship("recents", backref="users")
    last = relationship("last_songs", backref="users")
    fav = relationship("favourites", backref="users")
    playlist_song = relationship("playlist", backref="users")
    history = relationship("podcast_history", backref="users")


###create model for table to store tokens
class token(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    refresh_token = Column(String)
    access_token = Column(String)

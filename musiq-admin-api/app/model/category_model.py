from config.database import *
from sqlalchemy import Boolean,Column, Integer, String, TIMESTAMP,text
import sqlalchemy

###table creation for podcast's categories detail
class categories(Base):
    __tablename__ = "categories"
     
    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True)
    created_by = Column(Integer,nullable=True)
    updated_by = Column(Integer,nullable=True)
    is_delete = Column(Boolean,default=False)
    is_active = Column(Boolean,default=True)


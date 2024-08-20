from sqlalchemy import Column, Integer,TIME,ForeignKey,Boolean,String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from config.database import Base


class premium(Base):
    __tablename__ = "premium_model"
    
    id = Column(Integer, primary_key=True, index=True) 
    title = Column(String)
    price = Column(Integer)
    compare_price = Column(Integer,nullable=True)
    validity = Column(Integer,nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True, server_default=text('now()'))
    created_by = Column(Integer,nullable=True)
    updated_by = Column(Integer,nullable=True)
    is_delete = Column(Boolean,default=False)
    is_active = Column(Boolean,default=True)
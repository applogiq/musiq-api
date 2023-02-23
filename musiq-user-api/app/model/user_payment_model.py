from sqlalchemy import Boolean, Column,Integer, String,ForeignKey,JSON
from sqlalchemy.sql.sqltypes import TIMESTAMP
import datetime
from sqlalchemy_json import NestedMutableJson
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import sqlalchemy

from config.database import *

class UsersPayment(Base):
    __tablename__ = "user_payment"

    id = Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    payment_price=Column(Integer)
    payment_info = Column(JSON,nullable=True)
    premier_status=Column(String)
    razorpay_order_id =Column(String,nullable=True)
    razorpay_payment_id =Column(String,nullable=True)
    razorpay_signature =Column(String,nullable=True)
    payment_status = Column(String,nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    updated_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    created_by = Column(Integer,nullable=True)
    updated_by = Column(Integer,nullable=True)
    is_delete = Column(Boolean,default=False)
    is_active = Column(Boolean,default=True)


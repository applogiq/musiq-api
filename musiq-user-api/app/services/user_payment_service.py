from datetime import datetime

from model.user_model import *
from config.database import *
from utils.auth_bearer import *
from utils.payment_api import create_payment
from model.user_payment_model import *
from services.user_service import get_email


def create_payment_service(payment,db,email):
    temp = get_email(email,db)
    payment_details=create_payment(payment.payment_price,payment.premier_status)
    default=datetime.datetime.utcnow()
    if payment.premier_status=="free":
        subscription_date=None
        result = "No records"
    elif payment.premier_status=="1-month":
        subscription_date=default + datetime.timedelta(days=30)
        db_payment=UsersPayment(user_id=payment.user_id,
                            razorpay_order_id=payment_details["id"],
                            payment_price=payment.payment_price,
                            payment_info=payment_details,
                            premier_status=payment.premier_status,
                            created_by=temp.id
                            )
        db.add(db_payment)
        db.commit()
        result = db.query(UsersPayment.razorpay_order_id,UsersPayment.payment_info,UsersPayment.premier_status,UsersPayment.payment_price,UsersPayment.razorpay_order_id,UsersPayment.created_at).filter(UsersPayment.id == db_payment.id,UsersPayment.is_delete==False).first()
    elif payment.premier_status=="3-month":
        subscription_date=default + datetime.timedelta(day=90)
        db_payment=UsersPayment(user_id=payment.user_id,
                            razorpay_order_id=payment_details["id"],
                            payment_price=payment.payment_price,
                            payment_info=payment_details,
                            premier_status=payment.premier_status,
                            created_by=temp.id
                            )
        db.add(db_payment)
        db.commit()

        result = db.query(UsersPayment.razorpay_order_id,UsersPayment.payment_info,UsersPayment.premier_status,UsersPayment.payment_price,UsersPayment.payment_id,UsersPayment.created_at).filter(UsersPayment.id == db_payment.id,UsersPayment.is_delete==False).first()

    db_user=db.query(users).filter(users.id==payment.user_id,users.is_delete==False).first()
    db_user.premium_status=payment.premier_status
    db_user.subscription_end_date=subscription_date
    db.commit()
    return result

def callback(data,db):
   db_payment = db.query(UsersPayment).filter(UsersPayment.razorpay_order_id == data.razorpay_order_id,UsersPayment.is_delete==False).first()
   db_payment.razorpay_payment_id = data.razorpay_payment_id
   db_payment.razorpay_signature = data.razorpay_signature
   db_payment.payment_status = "success"
   db.commit()
   return db.query(UsersPayment).filter(UsersPayment.razorpay_order_id == data.razorpay_order_id,UsersPayment.is_delete==False).first()
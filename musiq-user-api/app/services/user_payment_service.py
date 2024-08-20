from datetime import datetime

from model.user_model import *
from config.database import *
from utils.auth_bearer import *
from utils.payment_api import create_payment
from model.user_payment_model import *
from services.user_service import get_email


def create_payment_service(payment,db,email):
    try:
        temp = get_email(email,db)

        if temp.id != payment.user_id:
            raise HTTPException(status_code=403, detail={"success": False,'message': "Unauthorized"})
    
        if payment.premier_status=="free":
            db_user=db.query(users).filter(users.id==payment.user_id,users.is_delete==False).first()
            db_user.premium_status=payment.premier_status
            db_user.subscription_end_date= None
            db.commit()
            result = "No records"
        else:
            payment_details=create_payment(payment.payment_price,payment.premier_status)
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
        
        return result
    except:
        return False

def callback_service(data,db,email):

    # try:
    temp = get_email(email,db)

    if temp.id != data.user_id:
        raise HTTPException(status_code=403, detail={"success": False,'message': "Unauthorized"})

    db_payment = db.query(UsersPayment).filter(UsersPayment.razorpay_order_id == data.razorpay_order_id,UsersPayment.is_delete==False).first()
    db_user=db.query(users).filter(users.id==data.user_id,users.is_delete==False).first()
    
    default=datetime.datetime.utcnow()
    subscription_date=default + datetime.timedelta(days=data.validity)
        
    db_payment.razorpay_payment_id = data.razorpay_payment_id
    db_payment.razorpay_signature = data.razorpay_signature
    db_payment.payment_status = "success"
    db_payment.updated_by = data.user_id
    db_payment.updated_at = default
    
    db_user.premium_status=data.premier_status
    db_user.subscription_end_date=subscription_date
    db_user.updated_at = default
    db.commit()

    return db.query(users).filter(users.id==data.user_id,users.is_delete==False).first()

    # except:
    #     return False

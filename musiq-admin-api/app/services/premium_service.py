from sqlalchemy.orm import Session
from fastapi import HTTPException
import datetime

from model.premium_status_model import premium
from services.admin_user_service import admin_get_email


###check premium name for avoid repitition
def premium_name_check(title,db):
    return db.query(premium).filter(premium.title == title,premium.is_delete == False).first()

###get all premium details
def premium_get_all(db: Session,limit):
    return db.query(premium).filter(premium.is_delete == False).order_by(premium.id).limit(limit).all()


###get single premium details by id
def premium_get_by_id(db: Session, id):
    return db.query(premium).filter(premium.id == id,premium.is_delete == False).first()


###enter new premium details
def premium_details(db,model,email):
    premiumname = premium_name_check(model.title,db)
    if premiumname:
        raise HTTPException(status_code=400, detail="premium is already register")
    temp = admin_get_email(email,db)
    
    db_premium = premium(title = model.title,
                    price = model.price,
                    compare_price = model.compare_price,
                    validity = model.validity,
                    created_by =temp.id)

    db.add(db_premium)
    db.commit()
    db.flush()
    premium_id = premium_get_by_id(db,db_premium.id)
    return premium_id


###update existing premium details
def premium_update(db,id,premium,email):
    temp = admin_get_email(email,db)
    db_premium = premium_get_by_id(db,id)
    if db_premium:
        if premium.title:
            premiumname = premium_name_check(premium.title,db)
            if premiumname:
                raise HTTPException(status_code=400, detail="premium is already register")
            
        for var,value in vars(premium).items():
              setattr(db_premium,var,value) if value else None                             
        db_premium.updated_by = temp.id
        db_premium.updated_at = datetime.now()
        db.commit()
        new_premium = premium_get_by_id(db,id)
        return new_premium
    return False


###delete single premium entirely by id
def premium_delete(db,id):
    temp = premium_get_by_id(db,id)
    if temp:
        temp.is_delete = True
        db.commit()
        return True
    return False
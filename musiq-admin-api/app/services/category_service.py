from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from model.category_model import categories
from services.admin_user_service import admin_get_email

def category_name_check(name,db):
    return db.query(categories).filter(categories.category_name == name,categories.is_delete == False).first()
# 
def category_get_all(db: Session):
    return db.query(categories).filter(categories.is_delete == False).all()

def category_get_by_id(db: Session, gen_id: int):
    return db.query(categories).filter(categories.id == gen_id,categories.is_delete == False).first()
  
def category_detail(db: Session,category,email):
    categoryname = category_name_check(category.category_name,db)
   
    if categoryname:
        raise HTTPException(status_code=400, detail="category is already register")
    
    temp = admin_get_email(email,db)
    db_category = categories(category_name = category.category_name,
                    is_delete = False,
                    created_by =temp.id,
                    is_active = True)

    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def category_update(db: Session,cat_id,category,email):
    user_temp1 = category_get_by_id(db,cat_id)
    if user_temp1:
        if category.category_name:
            tempname = category_name_check(category.category_name,db)
            if tempname:
                raise HTTPException(status_code=400, detail="category is already register")
            else:
                user_temp1.category_name = category.category_name  
        temp = admin_get_email(email,db)        
    
        user_temp1.updated_at = datetime.now()
        user_temp1.updated_by = temp.id

        db.commit()
        temp = category_get_by_id(db,cat_id)
        return temp
    else:
        raise False

def category_delete(db: Session,cat_id):
    temp = category_get_by_id(db,cat_id)
    if temp:
        temp.is_delete = True
        db.commit()
        return True
    return False
from sqlalchemy.orm import Session
from datetime import datetime
import shutil
import base64
from fastapi import HTTPException
import os
from config.database import DIRECTORY

from model.song_model import songs
from model.aura_model import aura
from services.admin_user_service import admin_get_email

def aura_detail(db: Session,auras,email):
    auraname =db.query(aura).filter(aura.aura_name == auras.aura_name,aura.is_delete == False).first()
    if auraname:
        raise HTTPException(status_code=400, detail="aura is already register")
    a ="AUR001"
    while db.query(aura).filter(aura.aura_id == a).first():
        a = "AUR00" + str(int(a[-1])+1)
    
    temp = admin_get_email(email,db)
    if auras.image:
        s = base64.b64decode(auras.image)
        filename1 = a+".png"
        file_location = f"{DIRECTORY}/aura/{filename1}"
        with open(file_location, "wb+") as f:
            f.write(s)  
        image = True
    else:
        image = False

    db_user = aura(aura_name = auras.aura_name,
                    aura_id = a,
                    is_image = image,
                    is_delete = False,
                    no_of_song = 0,
                    created_by = temp.id,
                    is_active = True)
    

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message":"data added"}


def aura_get_all(db: Session):
    return db.query(aura).filter(aura.is_delete == False).all()

def aura_get_by_id(db: Session, aura_id: int):
    auras = db.query(aura).filter(aura.id == aura_id,aura.is_delete == False).first()
    if auras:
        return auras
    else:
        return False

def aura_update(db: Session,aura_id: int,auras,email):
    user_temp1 = db.query(aura).filter(aura.id == aura_id,aura.is_delete == False).first()
    if user_temp1:
        if auras.aura_name:
            auraname =db.query(aura).filter(aura.aura_name == auras.aura_name,aura.is_delete == False).first()
            if auraname:
                raise HTTPException(status_code=400, detail="aura is already register")
            user_temp1.aura_name = auras.aura_name
        if auras.image:
            s = base64.b64decode(auras.image)
            filename1 = user_temp1.aura_id+".png"
            file_location = f"{DIRECTORY}/aura/{filename1}"
            with open(file_location, "wb+") as f:
                f.write(s)  
            user_temp1.is_image = 1

        temp = admin_get_email(email,db)
        user_temp1.updated_at = datetime.now()
        user_temp1.updated_by = temp.id

        db.commit()

        return {'message': "data updated"}
    else:
        raise HTTPException(status_code=404, detail="aura detail doesn't exist")

def aura_delete(db: Session,aura_id):
    user_temp = db.query(aura).filter(aura.id == aura_id,aura.is_delete == False).first()
    if user_temp:
        user_temp.is_delete = True
        db.commit()
        return {"message":"Deleted"}
    else:
        raise HTTPException(status_code=404, detail="aura details doesn't exist")
    
def delete_aura_image(db: Session,aura_id: int):
    user_temp = db.query(aura).filter(aura.id == aura_id,aura.is_delete == False,aura.is_image == True).first()
    if user_temp:
        user_temp.is_image = False

        file = user_temp.aura_id+".png"
        path = f"{DIRECTORY}/aura/{file}"
        os.remove(path)
        db.commit()
        return {'message': "aura image removed"}
    else:
        return {'message': "Check your id"}
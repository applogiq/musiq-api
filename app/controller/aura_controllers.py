from sqlalchemy.orm import Session
from datetime import datetime
import shutil
import base64
from fastapi import HTTPException
import os

from app.model.song_model import songs
from app.model.aura_model import aura

def aura_detail(db: Session,auras):
    auraname =db.query(aura).filter(aura.name == auras.name,aura.is_delete == 0).first()
    if auraname:
        raise HTTPException(status_code=400, detail="aura is already register")
    a ="AUR001"
    while db.query(aura).filter(aura.aura_id == a).first():
        a = "AUR00" + str(int(a[-1])+1)
    db_user = aura(name = auras.name,
                    aura_id = a,
                    is_image = 0,
                    is_delete = 0,
                    created_by = 1,
                    updated_by = 0,
                    is_active = 1)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message":"data added"}

def upload_aura_image_file(db: Session,aura_id: int,uploaded_file):
    user_temp = db.query(aura).filter(aura.id == aura_id,aura.is_delete == 0).first()
    if user_temp: 
        filename1 = user_temp.aura_id+".png"
        file_location = f"public/aura/{filename1}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(uploaded_file.file, file_object)  

        user_temp.is_image = 1
        db.commit()
        return {"info": f"file '{filename1}' saved at '{file_location}'"}
    else:
        raise HTTPException(status_code=404, detail="aura details doesn't exist")

def upload_base64_aura_file(db: Session,aura_id: int,img):
    user = db.query(aura).filter(aura.id == aura_id,aura.is_delete == 0).first()
    if user:
        s = base64.b64decode(img)
        filename1 = user.aura_id+".png"
        file_location = f"song/aura/{filename1}"
        with open(file_location, "wb+") as f:
            f.write(s)  

        user.is_image = 1
        db.commit()
        return {"info": f"file '{filename1}' saved at '{file_location}'"}
    else:
        raise HTTPException(status_code=404, detail="aura details doesn't exist")

def get_auras(db: Session):
    return db.query(aura).filter(aura.is_delete == 0).all()

def get_aura(db: Session, aura_id: int):
    auras = db.query(aura).filter(aura.id == aura_id,aura.is_delete == 0).first()
    if auras:
        return auras
    else:
        return False

def get_aura_image(db: Session,aura_id):
    temp = db.query(aura).filter(aura.id == aura_id,aura.is_delete == 0).first()
    if temp:
        user_temp = db.query(aura).filter(aura.id == aura_id,aura.is_delete == 0,aura.is_image == 1).first()
        if user_temp:
            link = f"http://127.0.0.1:8000/public/aura/{user_temp.aura_id}.png"
            return link
        else:
            raise HTTPException(status_code=404, detail="Image doesn't exist for this id")
    else:
        raise HTTPException(status_code=404, detail="check your id")

def aura_update(db: Session,aura_id: int,auras):
    user_temp1 = db.query(aura).filter(aura.id == aura_id,aura.is_delete == 0).first()
    if user_temp1:
        if auras.name:
            user_temp1.name = auras.name
            

        user_temp1.updated_at = datetime.now()
        user_temp1.updated_by = 1

        db.commit()

        return {'message': "data updated"}
    else:
        raise HTTPException(status_code=404, detail="aura detail doesn't exist")

def aura_delete(db: Session,aura_id):
    user_temp = db.query(aura).filter(aura.id == aura_id,aura.is_delete == 0).first()
    if user_temp:
        user_temp.is_delete = 1
        db.commit()
        return {"message":"Deleted"}
    else:
        raise HTTPException(status_code=404, detail="aura details doesn't exist")
    

def delete_aura_image(db: Session,aura_id: int):
    user_temp = db.query(aura).filter(aura.id == aura_id,aura.is_delete == 0,aura.is_image == 1).first()
    if user_temp:
        user_temp.is_image = 0

        file = user_temp.aura_id+".png"
        path = f"public/aura/{file}"
        os.remove(path)
        db.commit()
        return {'message': "aura image removed"}
    else:
        return {'message': "Check your id"}



    
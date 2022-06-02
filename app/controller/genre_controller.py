from sqlalchemy.orm import Session
from app.model.genre_model import genres
from datetime import datetime
from fastapi import HTTPException


def genre_detail(db: Session,genre):
    genrename =db.query(genres).filter(genres.name == genre.name,genres.is_delete == 0).first()
    a ="GN00"
    if genrename:
        raise HTTPException(status_code=400, detail="genre is already register")
    while db.query(genres).filter(genres.genre_id == a + genre.name[0:3].upper(),genres.is_delete == 0).first():
        a = "GN0" + str(int(a[-1])+1)
        
    db_genre = genres(name = genre.name,
                    genre_id = a+genre.name[0:3].upper(),
                    is_delete = 0,
                    created_by = 1,
                    updated_by = 0,
                    is_active = 1)

    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return {"message":"data added"}

def get_genres(db: Session):
    return db.query(genres).filter(genres.is_delete == 0).all()

def get_genre(db: Session, gen_id: int):
    temp = db.query(genres).filter(genres.id == gen_id,genres.is_delete == 0).first()
    if temp:
        return temp
    else:
        return False

def genre_update(db: Session,gen_id: int,genre):
    user_temp1 = db.query(genres).filter(genres.id == gen_id,genres.is_delete == 0).first()
    if user_temp1:
        pass
    else:
        raise HTTPException(status_code=404, detail="genre detail doesn't exist")

    if genre.name:
        a ="GN00"
       

        tempname = db.query(genres).filter(genres.name ==genre.name,genres.is_delete == 0).first()
        if tempname:
            raise HTTPException(status_code=400, detail="genre is already register")
        else:
            user_temp1.name = genre.name
            if db.query(genres).filter(genres.genre_id == a + genre.name[0:3].upper(),genres.is_delete == 0).first():
                a = "GN0" + str(int(a[-1])+1)
                user_temp1.genre_id = a + genre.name[0:3].upper()
            else: 
                user_temp1.genre_id = a +genre.name[0:3].upper()
    user_temp1.is_active = 1 
    user_temp1.is_delete = 0
    user_temp1.created_by = 1
    user_temp1.updated_at = datetime.now()
    user_temp1.updated_by = 1

    db.commit()

    return {'message': "data updated"}

def genre_delete(db: Session,gen_id):
    temp = db.query(genres).filter(genres.id == gen_id,genres.is_delete == 0).first()
    if temp:
        pass
    else:
        raise HTTPException(status_code=404, detail="genre detail doesn't exist")
    temp.is_delete = 1
    db.commit()
    return {"message":"Deleted"}

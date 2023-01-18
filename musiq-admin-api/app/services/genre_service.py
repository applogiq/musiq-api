from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from model.genre_model import genres
from services.admin_user_service import admin_get_email

###check genre name before enter to avoid repitition
def genre_name_check(name,db):
    return db.query(genres).filter(genres.genre_name == name,genres.is_delete == False).first()

###get all genre details
def genre_get_all(db: Session):
    return db.query(genres).filter(genres.is_delete == False).all()

###get genre details by it's id
def genre_get_by_id(db: Session, gen_id: int):
    return db.query(genres).filter(genres.id == gen_id,genres.is_delete == False).first()
  
###Enter new genre detail
def genre_detail(db: Session,genre,email):
    genrename = genre_name_check(genre.genre_name,db)
    if genrename:
        raise HTTPException(status_code=400, detail="genre is already register")
    genre_length = len(db.query(genres).all())
    if genre_length:
        b = genre_length+1
    else:
        b = 1
    a = "GN00"+str(b)
    # while db.query(genres).filter(genres.genre_id == a).first():
    #     a = "GN00" + str(int(a[-1])+1)
    temp = admin_get_email(email,db)
    db_genre = genres(genre_name = genre.genre_name,
                    genre_id = a,
                    is_delete = False,
                    created_by =temp.id,
                    updated_by = 0,
                    is_active = True)

    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


###update existing genre detail
def genre_update(db: Session,gen_id,genre,email):
    user_temp1 = genre_get_by_id(db,gen_id)
    if user_temp1:
        if genre.genre_name:
            tempname = genre_name_check(genre.genre_name,db)
            if tempname:
                raise HTTPException(status_code=400, detail="genre is already register")
            else:
                user_temp1.genre_name = genre.genre_name  
        temp = admin_get_email(email,db)        
    
        user_temp1.updated_at = datetime.now()
        user_temp1.updated_by = temp.id

        db.commit()
        temp = genre_get_by_id(db,gen_id)
        return temp
    else:
        raise False


###delete genre detail by it's id
def genre_delete(db: Session,gen_id):
    temp = genre_get_by_id(db,gen_id)
    if temp:
        temp.is_delete = True
        db.commit()
        return True
    return False



    

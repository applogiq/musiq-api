from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from app.model.favourite_model import favourites

def fav_song_detail(db: Session,fav):
    favname =db.query(favourites).filter(favourites.user_id == fav.user_id,favourites.song_id == fav.song_id).first()
    if favname:
        raise HTTPException(status_code=400, detail="This song is already register for this user") 
    else:
        db_fav = favourites(user_id = fav.user_id,
                            song_id = fav.song_id,
                            is_active = 1,
                            created_by = 1,
                            created_at = datetime.now()
                            )

        db.add(db_fav)
        db.commit()
        db.refresh(db_fav)
        return {"message":"data added"}

def fav_delete(db: Session,fav):
    favname =db.query(favourites).filter(favourites.user_id == fav.user_id,favourites.song_id == fav.song_id).first()
    if not favname:
            raise HTTPException(status_code=404, detail="favourites not found")
    else:
        db.delete(favname)
        db.commit()
        return {"message":"data deleted"}
    # else:
    #     raise HTTPException(status_code=404, detail="artist details doesn't exist")
    # user_temp.is_delete = 1
    # db.commit()
    # return {"message":"Deleted"}

def get_favourites(db: Session):
    return db.query(favourites).filter(favourites.is_active == 1).all()

def get_favourite(db: Session, fav_id: int):
    favs = db.query(favourites).filter(favourites.id == fav_id,favourites.is_active == 1).first()
    if favs:
        return favs
    else:
        return False

def get_favourite_songs(db: Session, user_id: int):
    favs = db.query(favourites).filter(favourites.user_id == user_id,favourites.is_active == 1).all()
    print(favs)
    s = []
    if favs:
        for i in range(0,len(favs)):
            s.append(favs[i].song_id)
        return s
    else:
        return False

from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from model.favourite_model import favourites
from model.song_model import songs
from model.user_model import users
from model.album_model import albums
from services.admin_user_service import admin_get_email

###Enter user's favourite detail
def fav_song_detail(db: Session,fav,email):
    favname =db.query(favourites).filter(favourites.user_id == fav.user_id,favourites.song_id == fav.song_id).first()
    if favname:
        raise HTTPException(status_code=400, detail={"success": False,"message":"this song is already register for this user"}) 
    temp = admin_get_email(email,db)
    db_fav = favourites(user_id = fav.user_id,
                        song_id = fav.song_id,
                        is_active = True,
                        created_by = temp.id,
                        created_at = datetime.now()
                        )
    db.add(db_fav)
    db.commit()
    db.refresh(db_fav)
    return db_fav

###remove favourite song from single user
def fav_delete(db: Session,fav):
    favname =db.query(favourites).filter(favourites.user_id == fav.user_id,favourites.song_id == fav.song_id).first()
    if not favname:
            raise HTTPException(status_code=404, detail={"success": False,"message":"favourites not found"})
    # else:
    db.delete(favname)
    db.commit()
    return True
    
###fetch all user's favourite songs detail
def fav_get_all(db: Session):
    return db.query(favourites).filter(favourites.is_active == True).all()


###fetch single user's favourite detail
def fav_get_by_userid(db: Session, user_id: int):
    favs = db.query(favourites).filter(favourites.user_id == user_id,favourites.is_active == True).all()
    s = []
    if favs:
        for i in range(0,len(favs)):
            s.append(favs[i].song_id)
            temp = db.query(songs.id,songs.song_name,albums.album_id,albums.album_name,albums.music_director_name).join(songs,albums.id == songs.album_id).filter(songs.id.in_(s)).all()
        return temp

    else:
        return False
